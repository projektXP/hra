import pygame
from abc import ABCMeta


class Thing(metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        self.x = x
        self.y = y
        self.room = room

        self.state_key = ['think', 'move']
        self.state_val = [True, False]

        self.canvas = pygame.Surface((room.square_size, room.square_size))

    def change_state(self):
        self.state_val[0], self.state_val[1] = self.state_val[1], self.state_val[0]

    def move_to(self, x, y):
        self.change_state()
        if not self.room.can_move_to(x, y) or not self.state_val[self.state_key.index('move')]:
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

