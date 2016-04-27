import pygame
from thing import Thing


class Start(Thing):
    def set_image(self):
        self.canvas = pygame.image.load('pictures/start.png')
