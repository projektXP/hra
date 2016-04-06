import random

from room import Room
from thing import Thing
from player import Player

class Monster(Thing):
    def __init__(self, room: Room, x=0, y=0, player: Player = None):
        super().__init__(room, x, y)

        self.player = player
        self.speed = 1
        
    def _step(self):
        nx, ny = 0, 0
        if self.x != self.player.x and self.y == self.player.y:
            if self.player.x > self.x:
                nx = self.x + self.speed
            else:
                nx = self.x - self.speed
        elif self.x == self.player.x and self.y != self.player.y:
            if self.player.y > self.y:
                ny = self.y + self.speed
            else:
                ny = self.y - self.speed
        elif self.x != self.player.x and self.y != self.player.y:
            if random.randrange(2):
                if self.player.x > self.x:
                    nx = self.x + self.speed
                else:
                    nx = self.x - self.speed
            else:
                if self.player.y > self.y:
                    ny = self.y + self.speed
                else:
                    ny = self.y - self.speed
        self.move_to(nx, ny)        


class FastMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)

        self.fast = True
        self.trackingPlayer = False

    def step(self):
        if self.player:
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            if dx**2 + dy**2 <= self.player.vision**2:
                self.trackingPlayer = True
                self._step()
            else:
                self.trackingPlayer = False



class SlowMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)

        self.fast = False
        self.trackingPlayer = True

    def step(self):
        if self.player:
            self._step()