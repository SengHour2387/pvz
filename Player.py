class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.level = 0

    def add_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def get_name(self):
        return self.name

    def add_level(self, level):
        self.level += level

    def get_level(self):
        return self.level