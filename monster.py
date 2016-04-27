import random

from moving_thing import MovingThing
from abc import ABCMeta, abstractmethod


class Monster(MovingThing, metaclass=ABCMeta):
    def follow_player(self):
        nx, ny = self.x, self.y
        if self.y == self.room.player.y and self.room.player.x == self.x:
            return

        if self.room.player.x > self.x:
            nx = self.x + 1
        elif self.room.player.x < self.x:
            nx = self.x - 1

        if self.room.player.y > self.y:
            ny = self.y + 1
        elif self.room.player.y < self.y:
            ny = self.y - 1

        if self.x != nx and self.y != ny:
            if random.randrange(2):
                nx = self.x
            else:
                ny = self.y

        self.start_moving(nx, ny)

    def step(self):
        if self.moving:
            self.move_a_bit()
        if not self.moving:
            self.think()

    @abstractmethod
    def think(self):
        pass


class Hunter(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((0, 255, 0))

        self.speed = 0.15 + round(random.randrange(7) / 100, 2)

    def think(self):
        if self.room.player:
            self.follow_player()


class Zombie(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((0, 128, 0))

        self.tracking_player = False
        self.speed = 0.1 + round(random.randrange(3) / 100, 2)

    def think(self):
        if self.room.player:
            if self.distance(self.room.player) <= self.vision:
                self.tracking_player = True
                self.follow_player()
            else:
                self.tracking_player = False


class Vampire(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((255, 255, 0))

        self.tracking_player = False
        self.speed = 0.1 + round(random.randrange(5) / 100, 2)

    def think(self):
        if self.room.player:
            if self.tracking_player or self.distance(self.room.player) <= self.vision:
                self.tracking_player = True
                self.follow_player()
