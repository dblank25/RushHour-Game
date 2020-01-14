class Path():

    def __init__(self, state):
        self.state = state
        self.path = []
        self.g = 0
        self.h = 0
        self.f = 0

    def add(self, states):
        if self.count(states):
            self.path.append(states)
        else:
            for state in states:
                self.path.append(state) 

    def get_path(self):
        return self.path

    def last(self):
        try:
            return self.path[-1]
        except:
            return []

    def clone(self, state):
        self.path.append(state)
        return self.path

    def count(self,state):
        state = str(state)
        if state[2] != '[':
            return True