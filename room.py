class Room:
    def __init__(self, square_size, width, height):
        # screen is divided into squares size x size
        self.square_size = square_size
        self.width = width
        self.height = height

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
        return 0 <= x < self.width and 0 <= y < self.height and self.map[y][x] is None
