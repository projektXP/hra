from moving_thing import MovingThing
from item import Item
import pygame


class Player(MovingThing):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((255, 0, 0))
        self.movements = {
            pygame.K_LEFT:  (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP:    (0, -1),
            pygame.K_DOWN:  (0, 1),
        }

    def can_move_to(self, x, y):
        return 0 <= x < self.room.width and 0 <= y < self.room.height and \
               (self.room.map[y][x] is None or isinstance(self.room.map[y][x], Item))

    def move_to(self, x, y):
        if self.can_move_to(x, y) and isinstance(self.room.map[y][x], Item):
            self.room.map[y][x].use(self)
        super().move_to(x, y)

    def move(self):
        keys = pygame.key.get_pressed()
        for key in self.movements:
            if keys[key]:
                self.move_to(
                    self.x + self.movements[key][0]*self.speed,
                    self.y + self.movements[key][1]*self.speed
                )
