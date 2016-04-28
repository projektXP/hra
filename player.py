from moving_thing import MovingThing
from item import Item
import pygame


class Player(MovingThing):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.movements = {
            pygame.K_LEFT:  (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP:    (0, -1),
            pygame.K_DOWN:  (0, 1),
        }

    def can_move_to(self, x, y):
        return 0 <= x < self.room.width and 0 <= y < self.room.height and \
               (self.room.dynamic_map[y][x] is None or self.room.dynamic_map[y][x].passable or isinstance(self.room.dynamic_map[y][x], Item)) and \
               (self.room.static_map[y][x] is None or self.room.static_map[y][x].passable)

    def start_moving(self, x, y):
        if self.can_move_to(x, y) and isinstance(self.room.dynamic_map[y][x], Item):
            self.room.dynamic_map[y][x].use(self)
        super().start_moving(x, y)

    def step(self):
        if self.moving:
            self.move_a_bit()

        if not self.moving:
            keys = pygame.key.get_pressed()
            for key in self.movements:
                if keys[key]:
                    self.start_moving(
                        self.x + self.movements[key][0],
                        self.y + self.movements[key][1],
                    )

    def set_image(self):
        self.canvas = pygame.image.load('pictures/player.png')
