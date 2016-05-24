import random
import pygame
from abc import ABCMeta, abstractmethod

from moving_thing import MovingThing
from utils import directions


class Monster(MovingThing, metaclass=ABCMeta):
    def follow_player(self):
        neighbours = [(x, y) for x, y in directions(self.x, self.y) if self.room.tracking_map[y][x] is not None]
        if neighbours:
            best_x, best_y = neighbours[0]
            for x, y in neighbours:
                if self.room.tracking_map[y][x] < self.room.tracking_map[best_y][best_x]:
                    best_x, best_y = x, y
            self.start_moving(best_x, best_y)

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

    def set_image(self):
        self.canvas = pygame.image.load('pictures/hunter.png')

        self.speed = 0.15 + round(random.randrange(7) / 100, 2)

    def think(self):
        if self.room.player:
            self.follow_player()


class Zombie(Monster):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)

        self.tracking_player = False
        self.speed = 0.1 + round(random.randrange(3) / 100, 2)

    def set_image(self):
        self.canvas = pygame.image.load('pictures/zombie.png')

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
        self.tracking_player = False
        self.speed = 0.1 + round(random.randrange(5) / 100, 2)

    def set_image(self):
        self.canvas = pygame.image.load('pictures/vampire.png')

    def think(self):
        if self.room.player:
            if self.tracking_player or self.distance(self.room.player) <= self.vision:
                self.tracking_player = True
                self.follow_player()
