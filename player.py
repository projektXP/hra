from moving_thing import MovingThing
from item import Item
import pygame
from collections import namedtuple

Point = namedtuple('Point', ['y', 'x'])


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
        self.update_tracking()

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

    def update_tracking(self):
        """
        Low-level function called every frame in order to update room.tracking_map via BFS algorithm.
        """
        self.room.tracking_map = [[None] * self.room.width for y in range(self.room.height)]
        visited = set()
        queue = [(Point(self.y, self.x), 0)]
        while queue:
            node, level = queue.pop(0)
            if node not in visited:
                visited.add(node)
                y, x = node.y, node.x
                self.room.tracking_map[y][x] = level
                for neighbour in {Point(y - 1, x),
                                  Point(y + 1, x),
                                  Point(y, x - 1),
                                  Point(y, x + 1)}:
                    if super().can_move_to(neighbour.x, neighbour.y) and neighbour not in visited:
                        queue.append((neighbour, level + 1))

    def set_image(self):
        self.canvas = pygame.image.load('pictures/player.png')
