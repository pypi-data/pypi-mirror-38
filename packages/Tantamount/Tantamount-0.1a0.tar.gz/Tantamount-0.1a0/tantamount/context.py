from threading import Lock, Thread
from sched import scheduler
from time import time
from threading import Event


class Context:

    def __init__(self):
        self._start = None
        self._state = None
        self._states = {}
        self._transitions = {}
        self._timeoutevent = None
        self._timeoutevents = {}

        # usually schdeuler is initialized with timefunc=time and
        # delayfunc=sleep. the problem is when using sleep, that if the
        # last event has been removed from scheduler using scheduler.cancel(),
        # the scheduler continues to sleep until the set delay has passed
        # altough no event exists that will be processed. the quick fix for
        # this is to use threading.Event.wait() instead. if Event.set() is
        # never called, the loop in scheduler.run behaves exactly like when
        # using sleep(). But with Event.set() a recalculation of the delay to
        # the next event can always be enforced. Thereafter, if Event.set() is
        # called after scheduler.cancel() the scheduler can adapt to the
        # new situation.
        self._delayfunc = Event()
        self._scheduler = scheduler(time, self._delayfunc.wait)
        self._schedulerthread = None

        self._lock_operate = Lock()
        self._firststartdone = False

    def setstartstate(self, stateid):
        self._state = self._states[stateid]
        self._start = self._state

    def addstate(self, stateid, state, groupid="_"):
        state.id = stateid
        state.groupid = groupid
        self._states[stateid] = state

    def addtransition(self, startstateid, transitionid, targetstateid):
        try:
            self._transitions[startstateid][transitionid] = targetstateid
        except KeyError:
            self._transitions[startstateid] = {}
            self._transitions[startstateid][transitionid] = targetstateid

    def addtimeoutevent(self, stateid, eventid, ms):
        try:
            if self._transitions[stateid][eventid]:
                self._timeoutevents[stateid] = (eventid, ms)
        except KeyError as e:
            print("Context.addtimeoutevent KeyError. stateid=" +
                  str(stateid) + ", eventid=" + str(eventid))
            raise e

    def firststart(self):
        if not self._firststartdone:
            self._firststartdone = True
            self._starttimeoutevent()
            self._state.operate()
        else:
            raise Exception("context.start must only be called once.")

    def _getnextstate(self, stateid, eventid):
        try:
            transition = self._transitions[stateid][eventid]
        except KeyError as e:
            print("Context.getnextstate KeyError. stateid=" +
                  str(stateid) + ", eventid=" + str(eventid))
            self._lock_operate.release()
            raise e

        try:
            nextstate = self._states[transition]
        except KeyError as e:
            print("Context.getnextstate KeyError. transition=" +
                  str(transition))
            self._lock_operate.release()
            raise e

        return nextstate

    def _starttimeoutevent(self):
        if self._timeoutevent is not None:
            raise Exception("context._starttimeoutevent has been called while "
                            "another timeoutevent has been still active.")

        try:
            (eventid, ms) = self._timeoutevents[self._state.id]
            self._timeoutevent = self._scheduler.enter(ms / 1000.0,
                                                       1, self.operate,
                                                       [eventid, True, ])
            threadname = type(self).__name__ + "|" + \
                         type(self._timeoutevent).__name__ + " (" + \
                         str(self._state.id) + ", " + str(eventid) + ")"
            self._schedulerthread = Thread(target=self._scheduler.run,
                                           name=threadname)
            self._schedulerthread.daemon = True
            self._schedulerthread.start()
        except KeyError:
            pass

    def _stoptimeoutevent(self):
        if self._timeoutevent is not None:
            try:
                self._scheduler.cancel(self._timeoutevent)
                self._delayfunc.set()
            except ValueError as x:
                pass
            self._timeoutevent = None

    def operate(self, eventid, timer=False):
        # three sources may call context.operate() - buttons, state.operate,
        # and timeout
        if self._lock_operate.acquire(False):
            self._operate(eventid)

    def _operate(self, eventid):
        self._stoptimeoutevent()
        self._state = self._getnextstate(self._state.id, eventid)
        self._starttimeoutevent()

        # lock needs to be released before state.operate() is called.
        # state.operate may call context.operate (-> internal events) ...
        self._lock_operate.release()
        self._state.operate()

    def stop(self):
        self._stoptimeoutevent()
        # self._schedulerthread.join() #not necessary any more - scheduler.run
        # stops immediatly after _stoptimeoutevent
