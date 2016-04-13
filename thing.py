import pygame
from abc import ABCMeta


class Thing(metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        self.x = x
        self.y = y
        self.room = room
        self.room.map[y][x] = self
        self.passable = False

        self.canvas = pygame.Surface((room.square_size, room.square_size))
        self.dictOfPic = dict()
        arrayKey = ['wall','hunter','vampire','zombie','floor','start','player','exit']
        arrayPic =['pictures/wall.png','pictures/hunter.png','pictures/vampire.png','pictures/zombie.png',
                   'pictures/floor.png','pictures/start.png','pictures/player.png','pictures/exit.png']
        for i in range(len(arrayKey)):
            self.dictOfPic[arrayKey[i]] = arrayPic[i]

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
        pass
