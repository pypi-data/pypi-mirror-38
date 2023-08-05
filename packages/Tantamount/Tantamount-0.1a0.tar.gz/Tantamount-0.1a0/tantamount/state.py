class State:
    def __init__(self, context):
        self.context = context
        self.id = None
        self.groupid = None

    def operate(self):
        raise NotImplementedError
