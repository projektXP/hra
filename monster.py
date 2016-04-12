import random

from thing import Thing
from abc import ABCMeta, abstractmethod


class Monster(Thing, metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

        self.state_key += ['attack']
        self.state_val += [False]
        self.speed = 1
        self.damage = 10

    def change_state(self):
        if abs(self.room.player.x - self.x) == 1 and abs(self.room.player.y - self.y) == 1:
             self.state_val = [False, False, True]
        elif self.state_val[2]:
            self.state_val = [True, False, False]
        else:
            self.state_val[0], self.state_val[1] = self.state_val[1], self.state_val[0]

    def move_to(self, x, y):
        self.change_state()
        if self.state_val[self.state_key.index('attack')]:
            self.attack()
            return
        if not self.room.can_move_to(x, y) or not self.state_val[self.state_key.index('move')]:
            return
        self.room.map[self.y][self.x] = None
        self.room.map[y][x] = self
        self.x, self.y = x, y

    def attack(self):
        self.room.player.health -= self.damage
        if self.room.player.health <= 0:
            print('Game Over')
            self.room.player.canvas.fill((64, 64, 64))

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

        self.damage = 5

    def step(self):
        if self.room.player:
            self.follow_player()


class Zombie(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((0, 128, 0))

        self.tracking_player = False
        self.damage = 20

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
        self.damage = 15

    def step(self):
        if self.room.player:
            if self.tracking_player or self.distance(self.room.player) <= self.room.player.vision:
                self.tracking_player = True
                self.follow_player()
