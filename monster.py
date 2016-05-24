import random
import pygame
from abc import ABCMeta, abstractmethod

from moving_thing import MovingThing
from utils import directions


class Monster(MovingThing, metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.attacking = False
        self.attack_start = None
        self.attack_time = 10
        self.damage = 0

    def follow_player(self):
        neighbours = [(x, y) for x, y in directions(self.x, self.y)
                      if self.room.tracking_map[y][x] is not None and self.can_move_to(x, y)]
        if neighbours:
            best_x, best_y = neighbours[0]
            for x, y in neighbours:
                if self.room.tracking_map[y][x] < self.room.tracking_map[best_y][best_x]:
                    best_x, best_y = x, y
            self.start_moving(best_x, best_y)

    def step(self):
        if self.moving:
            self.move_a_bit()
        elif self.attacking:
            self.attack_a_bit()
        if not self.moving and not self.attacking:
            self.think()

    @abstractmethod
    def think(self):
        pass

    def start_attacking(self):
        if self.attacking:
            return

        self.attacking = True
        self.attack_start = self.room.game.time

    def can_attack(self):
        return self.distance(self.room.player) == 1

    def attack_a_bit(self):
        if self.room.game.time - self.attack_start >= self.attack_time:
            self.room.player.take_damage(self.damage)
            self.attack_start = None
            self.attacking = False


class Hunter(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

        self.speed = 0.15 + round(random.randrange(7) / 100, 2)
        self.damage = 5
        self.attack_time = 10

    def set_image(self):
        self.canvas = pygame.image.load('pictures/hunter.png')

    def think(self):
        if self.room.player:
            if self.can_attack():
                self.start_attacking()
            else:
                self.follow_player()


class Zombie(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

        self.tracking_player = False
        self.speed = 0.1 + round(random.randrange(3) / 100, 2)
        self.damage = 10
        self.attack_time = 20

    def set_image(self):
        self.canvas = pygame.image.load('pictures/zombie.png')

    def think(self):
        if self.room.player:
            if self.can_attack():
                self.start_attacking()
            elif self.distance(self.room.player) <= self.vision:
                self.tracking_player = True
                self.follow_player()
            else:
                self.tracking_player = False


class Vampire(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.tracking_player = False
        self.speed = 0.1 + round(random.randrange(5) / 100, 2)
        self.damage = 15
        self.attack_time = 15

    def set_image(self):
        self.canvas = pygame.image.load('pictures/vampire.png')

    def think(self):
        if self.room.player:
            if self.can_attack():
                self.start_attacking()
            elif self.tracking_player or self.distance(self.room.player) <= self.vision:
                self.tracking_player = True
                self.follow_player()
