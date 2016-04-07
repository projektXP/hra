import pygame


class Thing:
    def __init__(self, room, x=0, y=0):
        self.x = x
        self.y = y
        self.room = room
        self.room.map[y][x] = self

        self.canvas = pygame.Surface((room.square_size, room.square_size))

    def move_to(self, x, y):
        if not self.room.can_move_to(x, y):
            return
        self.room.map[self.y][self.x] = None
        self.room.map[y][x] = self
        self.x, self.y = x, y

    def distance(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return dx + dy

    def draw(self):
        return self.canvas

