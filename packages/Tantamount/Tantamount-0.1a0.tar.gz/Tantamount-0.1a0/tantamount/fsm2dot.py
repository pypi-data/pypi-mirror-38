class GetDotNotation():
    def __init__(self, context, graphname="fsm", getStateId=None,
                 getStateName=None, getTransitionName=None,
                 internaleventprefix="_", internaleventreturn="_RETURN"):
        self.context = context
        self.graphname = graphname
        self.internaleventprefix = internaleventprefix
        self.internaleventreturn = internaleventreturn

        if getStateId is None:
            self.getStateId = lambda x: str(x)
        else:
            self.getStateId = getStateId

        if getStateName is None:
            self.getStateName = lambda x: str(x)
        else:
            self.getStateName = getStateName

        if getTransitionName is None:
            self.getTransitionName = lambda x: str(x)
        else:
            self.getTransitionName = getTransitionName

    def _states2groups(self, states):
        groups = {}

        for id, state in states.items():
            try:
                groups[state.groupid].append(state)
            except KeyError:
                groups[state.groupid] = []
                groups[state.groupid].append(state)

        return groups

    def _state2dot(self, state, identlevel=1):
        statename = self.getStateName(state)
        options = 'label="' + statename + '"'
        if self.context._start.id == state:
            options += ', peripheries=2'
        dot = ' ' * 4 * (identlevel) + self.getStateId(state) + \
              ' [' + options + '];\n'
        return dot

    def _getstates(self):
        dot = "    // adding all states with their internal id and their " \
              "human readable name\n"

        groups = self._states2groups(self.context._states)
        for groupid, states in groups.items():
            identlevel = 1
            if not groupid == "_":
                identlevel = 2
                dot += '    subgraph cluster_' + groupid + ' {\n'
                dot += '        label="' + groupid + '"\n'
            for state in states:
                dot += self._state2dot(state.id, identlevel)
            if not groupid == "_":
                dot += '    }\n'

        dot += "\n"
        return dot

    def _getdirectededges(self):
        dot = "    //adding all directed edges\n"
        for startstateid, _temp in self.context._transitions.items():
            for transitionid, targetstateid in _temp.items():
                transitionname = self.getTransitionName(transitionid)

                if transitionname == self.internaleventreturn:
                    options = 'color = "gray"'
                elif transitionname[:len(self.internaleventprefix)] == \
                        self.internaleventprefix:
                    try:
                        t = self.context._timeoutevents[startstateid]
                        if t[0] == transitionid:
                            s = t[1] / 1000.0
                            transitionname += " [{0:g}s]".format(s)
                    except KeyError:
                        pass
                    options = 'label="' + transitionname + \
                              '" color="darkslategray" fontcolor="darkslategray"'
                else:
                    options = 'label="' + transitionname + '"'
                dot += '    ' + self.getStateId(startstateid) + ' -> ' + \
                       self.getStateId(targetstateid) + ' [' + options + '];\n'
        dot += "\n"
        return dot

    def _getkey(self):
        dot = '''\
    subgraph cluster_key_20151006 {
        label = "Key";

        init_20151006[label = "Start", peripheries = 2];
        key1_20151006[shape = plaintext, style = solid,
                        label = "Initial State\\r", width = 3.5]

        source1_20151006[label = "Source"];
        target1_20151006[label = "Target"];
        source1_20151006->target1_20151006[label = "name"];
        key2_20151006[shape = plaintext, style = solid,
                        label = "External Event\\r", width = 3.5]

        source2_20151006[label = "Source"];
        target2_20151006[label = "Target"];
        source2_20151006->target2_20151006[label = "name"
        color = "darkslategray"
        fontcolor = "darkslategray"];
        key3_20151006[shape = plaintext, style = solid,
                        label = "Internal Event\\r", width = 3.5]

        source3_20151006[label = "Source"];
        target3_20151006[label = "Target"];
        source3_20151006->target3_20151006[label = "", color = "gray",
                                            fontcolor = "gray"];
        key4_20151006[shape = plaintext, style = solid,
                        label = "Int. Event _RETURN\\r", width = 3.5]

        {rank = source; key1_20151006 key2_20151006
                        key3_20151006 key4_20151006}
    }\
        \n'''
        return dot

    def getdotnotation(self):
        dot = "digraph fsm {\n"
        dot += '    label="' + self.graphname + '"\n'
        dot += '    labelloc=t;\n'
        dot += '    rankdir=LR;\n'
        dot += '\n'
        dot += self._getstates()
        dot += '\n'
        dot += self._getdirectededges()
        dot += '\n'
        dot += self._getkey()
        dot += '\n'
        dot += "}\n"

        return dot
