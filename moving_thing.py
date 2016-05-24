from thing import Thing, Shadow
from abc import ABCMeta
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class MovingThing(Thing, metaclass=ABCMeta):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.vision = 10
        self.speed = 0.1

        self.moving = False
        self.destination = None
        self.moving_progress = 0

    def get_relative_position_to_draw(self):
        if not self.moving:
            return self.x, self.y
        else:
            rel_x = self.x + (self.destination.x - self.x) * self.moving_progress
            rel_y = self.y + (self.destination.y - self.y) * self.moving_progress
            return rel_x, rel_y

    @classmethod
    def class_can_move_to(cls, x, y, room):
        return 0 <= x < room.width and 0 <= y < room.height and \
               (room.dynamic_map[y][x] is None or room.dynamic_map[y][x].passable) and \
               (room.static_map[y][x] is None or room.static_map[y][x].passable)

    def can_move_to(self, x, y):
        return self.class_can_move_to(x, y, self.room)

    def start_moving(self, x, y):
        """
        High-level command to start moving, called in thinking phase of monsters / player.
        Sets the moving flag, creates Shadow at the destination.
        """
        if not self.can_move_to(x, y):
            return

        if self.moving:
            return

        self.moving = True
        self.destination = Point(x, y)
        self.moving_progress = 0
        self.room.dynamic_map[y][x] = Shadow(self.room, x, y)

    def move_a_bit(self):
        """
        Low-level function called every frame.
        """
        self.moving_progress += self.speed

        if self.moving_progress >= 1:
            self.room.dynamic_map[self.y][self.x] = None
            self.room.dynamic_map[self.destination.y][self.destination.x] = self
            self.x, self.y = self.destination.x, self.destination.y

            self.moving = False
            self.destination = None
            self.moving_progress = 0

