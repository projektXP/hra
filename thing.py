import pygame
from abc import ABCMeta


class Thing(metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        self.x = x
        self.y = y
        self.room = room

        self.canvas = pygame.Surface((room.square_size, room.square_size))

    def can_move_to(self, x, y):
        return 0 <= x < self.room.width and 0 <= y < self.room.height and self.room.map[y][x] is None

    def move_to(self, x, y):
        if not self.can_move_to(x, y):
            return
        self.room.map[self.y][self.x] = None
        self.room.map[y][x] = self
        self.x, self.y = x, y

    def distance(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return abs(dx) + abs(dy)

    def draw(self):
        return self.canvas

