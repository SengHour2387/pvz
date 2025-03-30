class Position:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def copy(self):
        return Position(self.x,self.y)