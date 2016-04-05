import random

from room import Room
from thing import Thing
from player import Player

class Monster(Thing):
    def __init__(self, room: Room, x=0, y=0, player: Player = None):
        super().__init__(room, x, y)

        self.player = player



class FastMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)
        super().__init__(room, x, y, player)

        self.fast = True
        self.track = False

    def step(self):
        if self.player:
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            if dx <= self.player.vision >= dy:
                self.track = True
                if self.x != self.player.x and self.y == self.player.y:
                    nx = self.x + dx / dx
                elif self.x == self.player.x and self.y != self.player.y:
                    ny = self.y + dy / dy
                elif self.x != self.player.x and self.y != self.player.y:
                    if random.randrange(2):
                        nx = self.x + dx / dx
                    else:
                        ny = self.y + dy / dy
                self.move_to(nx, ny)
            else:
                self.track = False



class SlowMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)

        self.fast = False
        self.track = True

    def step(self):
        if self.player:
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            if self.x != self.player.x and self.y == self.player.y:
                nx = self.x + dx / dx
            elif self.x == self.player.x and self.y != self.player.y:
                ny = self.y + dy / dy
            elif self.x != self.player.x and self.y != self.player.y:
                if random.randrange(2):
                    nx = self.x + dx / dx
                else:
                    ny = self.y + dy / dy
            self.move_to(nx, ny)