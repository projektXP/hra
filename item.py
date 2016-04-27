import pygame
from thing import Thing
from abc import ABCMeta, abstractmethod


class Item(Thing, metaclass=ABCMeta):
    @abstractmethod
    def use(self, player):
        pass


class SpeedBoost(Item):
    def use(self, player):
        player.speed *= 2

    def set_image(self):
        self.canvas = pygame.Surface((self.room.square_size, self.room.square_size))
        self.canvas.fill((0, 0, 255))


class Fog(Item):
    def use(self, player):
        player.vision = 5

    def set_image(self):
        self.canvas = pygame.Surface((self.room.square_size, self.room.square_size))
        self.canvas.fill((255, 0, 0))
