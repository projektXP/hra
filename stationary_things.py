import pygame
from thing import Thing


class Wall(Thing):
    def set_image(self):
        self.canvas = pygame.image.load('pictures/wall.png')


class Start(Thing):
    def set_image(self):
        self.canvas = pygame.image.load('pictures/start.png')


class Exit(Thing):
    def set_image(self):
        self.canvas = pygame.image.load('pictures/exit.png')
