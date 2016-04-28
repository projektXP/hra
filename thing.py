import pygame
from abc import ABCMeta, abstractmethod


class Thing(metaclass=ABCMeta):
    passable = False

    def __init__(self, room, x=0, y=0):
        self.x = x
        self.y = y
        self.room = room

        self.canvas = None
        self.set_image()

    @abstractmethod
    def set_image(self):
        pass

    def get_relative_position_to_draw(self):
        return self.x, self.y

    def distance(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return abs(dx) + abs(dy)

    def draw(self):
        return self.canvas


class Shadow(Thing):
    """
    Placeholder class, destination of moving things.
    Ensures that only one moving-thing will start to move to one destination.
    """
    def set_image(self):
        self.canvas = pygame.Surface((0, 0))
