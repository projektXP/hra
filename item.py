import pygame
from thing import Thing
from abc import ABCMeta, abstractmethod


class Item(Thing, metaclass=ABCMeta):
    @abstractmethod
    def use(self, player):
        pass


class SpeedBoost(Item):
    def use(self, player):
        player.speed *= 1.5

    def set_image(self):
        self.canvas = pygame.image.load('pictures/speed.png')


class Fog(Item):
    def use(self, player):
        player.vision = 2

    def set_image(self):
        self.canvas = pygame.image.load('pictures/fog.png')
