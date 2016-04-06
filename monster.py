import random

from thing import Thing
from abc import ABCMeta, abstractmethod


class Monster(Thing, metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

        self.speed = 1
        
    def follow_player(self):
        nx, ny = self.x, self.y
        if self.y == self.room.player.y and self.room.player.x == self.x:
            return

        if self.room.player.x > self.x:
            nx = self.x + self.speed
        elif self.room.player.x < self.x:
            nx = self.x - self.speed

        if self.room.player.y > self.y:
            ny = self.y + self.speed
        elif self.room.player.y < self.y:
            ny = self.y - self.speed

        if self.x != nx and self.y != ny:
            if random.randrange(2):
                nx = self.x
            else:
                ny = self.y

        self.move_to(nx, ny)

    @abstractmethod
    def step(self):
        pass


class Hunter(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((0, 255, 0))

    def step(self):
        if self.room.player:
            self.follow_player()


class Zombie(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((0, 128, 0))

        self.tracking_player = False

    def step(self):
        if self.room.player:
            if self.distance(self.room.player) <= self.room.player.vision:
                self.tracking_player = True
                self.follow_player()
            else:
                self.tracking_player = False


class Vampire(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((255, 255, 0))

        self.tracking_player = False

    def step(self):
        if self.room.player:
            if self.tracking_player or self.distance(self.room.player) <= self.room.player.vision:
                self.tracking_player = True
                self.follow_player()
