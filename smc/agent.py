""" Class for Agent """


class Agent:
    def __init__(self, init_x, init_y):
        """ Constructor for Agent class """
        self.x = init_x
        self.y = init_y


class AgentTrajectories:
    def __init__(self):
        self.xs = []
        self.ys = []

    def add_point(self, x, y):
        """ adds a new point to the trajectory """
        self.xs.append(x)
        self.ys.append(y)
