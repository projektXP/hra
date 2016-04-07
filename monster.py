import random

from room import Room
from thing import Thing
from player import Player


class Monster(Thing):
    def __init__(self, room: Room, x=0, y=0, player: Player = None):
        super().__init__(room, x, y)

        self.player = player
        self.speed = 1
        
    def follow_player(self):
        nx, ny = self.x, self.y
        if self.y == self.player.y and self.player.x == self.x:
            return

        if self.player.x > self.x:
            nx = self.x + self.speed
        elif self.player.x < self.x:
            nx = self.x - self.speed

        if self.player.y > self.y:
            ny = self.y + self.speed
        elif self.player.y < self.y:
            ny = self.y - self.speed

        if self.x != nx and self.y != ny:
            if random.randrange(2):
                nx = self.x
            else:
                ny = self.y

        self.move_to(nx, ny)


class Hunter(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)
        self.canvas.fill((0, 255, 0))

    def step(self):
        if self.player:
            self.follow_player()


class Zombie(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)
        self.canvas.fill((0, 128, 0))

        self.tracking_player = False

    def step(self):
        if self.player:
            if self.distance(self.player) <= self.player.vision:
                self.tracking_player = True
                self.follow_player()
            else:
                self.tracking_player = False


class Vampire(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)
        self.canvas.fill((255, 255, 0))

        self.tracking_player = False

    def step(self):
        if self.player:
            if self.tracking_player or self.distance(self.player) <= self.player.vision:
                self.tracking_player = True
                self.follow_player()
