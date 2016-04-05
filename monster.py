from thing import Thing
from player import Player

class Monster(Thing):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y)

        self.player = player

class FastMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)

        self.fast = True
        self.track = False

    def step(self):
        pass

class SlowMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)

        self.fast = False
        self.track = True

    def step(self):
        if self.player and (self.x != self.player.x or self.y != self.player.y):
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            if dx + dy == dx or dx + dy == dy:
                pass
            else:
