import pygame
from thing import Thing


class Wall(Thing):
    def set_image(self):
        self.canvas = pygame.image.load('pictures/wall.png')
