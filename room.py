from player import Player
from monster import Vampire, Hunter, Zombie


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

    def can_move_to(self, x, y):
        try:
            return 0 <= x < self.width and 0 <= y < self.height and self.map[y][x] is None
        except IndexError:
            print(x, y)

    def load_from_file(self, filename):
        self.map = []
        char_to_thing = {
            '.': lambda room, x, y: None,
            'P': Player,
            'V': Vampire,
            'H': Hunter,
            'Z': Zombie,
        }
        col_count = 0
        for y, line in enumerate(open(filename)):
            line = line.strip()
            if y == 0:
                col_count = len(line)
            elif col_count != len(line):
                raise RuntimeError("invalid input file: jagged lines")

            this_row = []
            for x, ch in enumerate(line):
                if ch not in char_to_thing:
                    raise RuntimeError("invalid input file: character {} not mapped to any object".format(ch))

                thing = char_to_thing[ch](self, x, y)
                if isinstance(thing, Player):
                    self.player = thing
                this_row.append(thing)

            self.map.append(this_row)

        self.height = len(self.map)
        self.width = col_count
