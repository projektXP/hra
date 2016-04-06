import random

from room import Room
from thing import Thing
from player import Player

class Monster(Thing):
    def __init__(self, room: Room, x=0, y=0, player: Player = None):
        super().__init__(room, x, y)

        self.player = player
        self.speed = 1
        
    def followPlayer(self):
        nx, ny = self.x, self.y
        if self.y == self.player.y and self.player.x == self.x:
            return

        if self.y == self.player.y:
            if self.player.x > self.x:
                nx = self.x + self.speed
            else:
                nx = self.x - self.speed

        elif self.x == self.player.x:
            if self.player.y > self.y:
                ny = self.y + self.speed
            else:
                ny = self.y - self.speed

        else:
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



class AlwaysFollowingMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)
        self.canvas.fill((0, 255, 0))

        self.fast = False
        self.trackingPlayer = True

    def step(self):
        if self.player:
            self.followPlayer()



class FollowingOnSightOnlyMonster(Monster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)
        self.canvas.fill((0, 128, 0))

        self.fast = True
        self.trackingPlayer = False

    def step(self):
        if self.player:
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            if dx**2 + dy**2 <= self.player.vision**2:
                self.trackingPlayer = True
                self.followPlayer()
            else:
                self.trackingPlayer = False



class OnceOnSightFollowingMonster(FollowingOnSightOnlyMonster):
    def __init__(self, room, x=0, y=0, player=None):
        super().__init__(room, x, y, player)
        self.canvas.fill((255, 255, 0))

    def step(self):
        if self.player:
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            if self.trackingPlayer or dx**2 + dy**2 <= self.player.vision**2:
                self.trackingPlayer = True
                self.followPlayer()
