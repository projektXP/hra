from thing import Thing


class Monster(Thing):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

class FastMonster(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

        self.fast = True

    def step(self):
        pass

class SlowMonster(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

        self.fast = False

    def step(self):
        pass