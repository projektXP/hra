import pygame
from thing import Thing


class Wall(Thing):
    passable = False

    def set_image(self):
        self.canvas = pygame.image.load('pictures/wall.png')


class Start(Thing):
    passable = True

    def set_image(self):
        self.canvas = pygame.image.load('pictures/start.png')


class Exit(Thing):
    passable = True

    def set_image(self):
        self.canvas = pygame.image.load('pictures/exit.png')


class Floor(Thing):
    passable = True

    def set_image(self):
        self.canvas = pygame.image.load('pictures/floor.png')
