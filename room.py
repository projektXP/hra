from player import Player
from monster import Vampire, Hunter, Zombie
from item import SpeedBoost, Fog
from wall import Wall
from exit import Exit
from start import Start

class Room:
    def __init__(self, square_size, width=0, height=0):
        # screen is divided into squares size x size
        self.square_size = square_size
        self.width = width
        self.height = height

        self.player = None
        self.map = [[None] * width for x in range(height)]

    def canvas_size(self):
        return self.width * self.square_size, self.height * self.square_size

    def abs_coords(self, x, y):
        return x * self.square_size, y * self.square_size

    def things_of_class(self, classname):
        for row in self.map:
            for thing in row:
                if isinstance(thing, classname):
                    yield thing

    def load_from_file(self, filename):
        self.map = []
        char_to_thing = {
            '.': lambda room, x, y: None,
            'P': Player,
            'V': Vampire,
            'H': Hunter,
            'Z': Zombie,
            's': SpeedBoost,
            'f': Fog,
            '#': Wall,
            'E': Exit,
            'S': Start,
        }
        col_count = 0
        with open(filename) as f:
            for y, line in enumerate(f):
                line = line.strip()

                if y == 0:
                    col_count = len(line)
                elif col_count != len(line):
                    raise RuntimeError("invalid input file: jagged lines")

                this_row = []
                for x, ch in enumerate(line):
                    if ch not in char_to_thing:
                        raise RuntimeError("invalid input file: character '{}' not mapped to any object".format(ch))

                    thing = char_to_thing[ch](self, x, y)
                    if isinstance(thing, Player):
                        if self.player is not None:
                            raise RuntimeError("player already present in room")
                        self.player = thing

                    this_row.append(thing)

                self.map.append(this_row)

        if self.player is None:
            raise RuntimeError("no player present in room")
        self.height = len(self.map)
        self.width = col_count
