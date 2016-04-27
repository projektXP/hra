import pygame
from thing import Thing


class Exit(Thing):
    def set_image(self):
        self.canvas = pygame.image.load('pictures/exit.png')
