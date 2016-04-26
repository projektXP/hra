from thing import Thing
from abc import ABCMeta


class MovingThing(Thing, metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.vision = 10
        self.speed = 1

    def can_move_to(self, x, y):
        return 0 <= x < self.room.width and 0 <= y < self.room.height and self.room.map[y][x] is None

    def move_to(self, x, y):
        if not self.can_move_to(x, y):
            return
        self.room.map[self.y][self.x] = None
        self.room.map[y][x] = self
        self.x, self.y = x, y

