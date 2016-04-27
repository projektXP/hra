from queue import Queue

from player import Player
from monster import Vampire, Hunter, Zombie, Monster
from item import SpeedBoost, Fog
from stationary_things import Wall, Exit, Start, Floor
from utils import directions


class Room:
    def __init__(self, game, square_size, width=0, height=0):
        self.game = game
        # screen is divided into squares size x size
        self.square_size = square_size
        self.width = width
        self.height = height

        self.player = None
        self.static_map = [[None] * width for y in range(height)]
        self.dynamic_map = [[None] * width for y in range(height)]
        self.tracking_map = [[None] * width for y in range(height)]

    def canvas_size(self):
        return self.width * self.square_size, self.height * self.square_size

    def abs_coords(self, x, y):
        return x * self.square_size, y * self.square_size

    def things_of_class(self, classname, static_map):
        if static_map:
            map = self.static_map
        else:
            map = self.dynamic_map

        for row in map:
            for thing in row:
                if isinstance(thing, classname):
                    yield thing

    def load_from_file(self, filename):
        self.static_map = []
        self.dynamic_map = []

        char_to_thing_static = {
            '.': Floor,
            '#': Wall,
            'E': Exit,
            'S': Start,
        }

        char_to_thing_dynamic = {
            'V': Vampire,
            'H': Hunter,
            'Z': Zombie,
            's': SpeedBoost,
            'f': Fog,
        }

        col_count = 0
        with open(filename) as f:
            for y, line in enumerate(f):
                line = line.strip()

                if y == 0:
                    col_count = len(line)
                elif col_count != len(line):
                    raise RuntimeError("invalid input file: jagged lines")

                this_row_static = []
                this_row_dynamic = []

                for x, ch in enumerate(line):
                    if ch in char_to_thing_static:
                        thing = char_to_thing_static[ch](self, x, y)
                        this_row_static.append(thing)
                        this_row_dynamic.append(None)

                        if isinstance(thing, Start):
                            if self.player is not None:
                                raise RuntimeError("starting position already present in room")
                            self.player = Player(self, x, y)
                            this_row_dynamic[-1] = self.player

                    elif ch in char_to_thing_dynamic:
                        thing = char_to_thing_dynamic[ch](self, x, y)
                        this_row_dynamic.append(thing)
                        this_row_static.append(Floor(self, x, y))
                    else:
                        raise RuntimeError("invalid input file: character '{}' not mapped to any object".format(ch))

                self.static_map.append(this_row_static)
                self.dynamic_map.append(this_row_dynamic)

        if self.player is None:
            raise RuntimeError("no starting position present in room")
        self.height = len(self.static_map)
        self.width = col_count
        self.tracking_map = [[None] * self.width for y in range(self.height)]

    def update_tracking(self):
        """
        Low-level function called every frame in order to update room.tracking_map via BFS algorithm.
        """
        self.tracking_map = [[None] * self.width for y in range(self.height)]
        queue = Queue()
        queue.put((self.player.x, self.player.y))
        self.tracking_map[self.player.y][self.player.x] = 0

        while not queue.empty():
            x, y = queue.get()
            level = self.tracking_map[y][x]

            for nx, ny in directions(x, y):
                if Monster.class_can_move_to(nx, ny, self) and self.tracking_map[ny][nx] is None:
                    self.tracking_map[ny][nx] = level + 1
                    queue.put((nx, ny))
