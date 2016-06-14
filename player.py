from moving_thing import MovingThing
from item import Item
from stationary_things import Exit
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
        self.health = 100
        self.speed *= 1.3
        self.vision = 4

    @classmethod
    def class_can_move_to(cls, x, y, room):
        return 0 <= x < room.width and 0 <= y < room.height and \
               (room.dynamic_map[y][x] is None or room.dynamic_map[y][x].passable or isinstance(room.dynamic_map[y][x], Item)) and \
               (room.static_map[y][x] is None or room.static_map[y][x].passable)

    def start_moving(self, x, y):
        if self.can_move_to(x, y) and isinstance(self.room.dynamic_map[y][x], Item):
            self.room.dynamic_map[y][x].use(self)
        super().start_moving(x, y)

    def step(self):
        if isinstance(self.room.static_map[self.y][self.x], Exit):
            self.room.game.start()

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

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.canvas = pygame.image.load('pictures/dead_player.png')
        self.room.game.game_over = True
