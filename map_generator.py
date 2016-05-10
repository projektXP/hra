"""
1) Generate sub-rooms
    - select sub-room
    - create wall in sub-room with entrance
    - add 2 new sub-rooms to list

2) Generate interiors of sub-rooms
    - monsters, items

3) Put start at random place

4) Put exit at place that is as far as it gets
"""

import random
from itertools import cycle
from queue import Queue

WALL_VERTICAL = 0
WALL_HORIZONTAL = 1

WALL_CHARACTER = "#"
EMPTY_CHARACTER = "."
START_CHARACTER = "S"
EXIT_CHARACTER = "E"
VAMPIRE_CHARACTER = "V"
ZOMBIE_CHARACTER = "Z"
HUNTER_CHARACTER = "H"
SPEED_CHARACTER = "s"
FOG_CHARACTER = "f"


class MapGenerator:
    def __init__(self, min_subroom_dimension):
        self.min_subroom_dimension = min_subroom_dimension
        self.min_splittable_subroom_dimension = 2 * self.min_subroom_dimension + 1
        self.width, self.height = 0, 0
        self.room_map = []
        self.set_up_empty_room_with_sentinels()

    def set_up_empty_room_with_sentinels(self):
        self.width, self.height = 10 + random.randint(0, 20), 10 + random.randint(0, 10)

        self.room_map = [[WALL_CHARACTER for x in range(self.width)] for y in range(self.height)]

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.room_map[y][x] = EMPTY_CHARACTER

    def split_subroom_vertically(self, x, y, w, h):
        wall_x = random.randint(x + self.min_subroom_dimension, x + w - 1 - self.min_subroom_dimension)

        wall_start_y = y
        wall_end_y = y + h - 1

        for wall_y in range(wall_start_y, wall_end_y + 1):
            self.room_map[wall_y][wall_x] = "#"

        door_generated = False

        if self.room_map[wall_start_y - 1][wall_x] == EMPTY_CHARACTER:
            self.room_map[wall_start_y][wall_x] = EMPTY_CHARACTER
            door_generated = True

        if self.room_map[wall_end_y + 1][wall_x] == EMPTY_CHARACTER:
            self.room_map[wall_end_y][wall_x] = EMPTY_CHARACTER
            door_generated = True

        if not door_generated:
            self.room_map[random.randint(wall_start_y, wall_end_y)][wall_x] = EMPTY_CHARACTER

        new_subroom_1 = (x, y, wall_x - x, h)
        new_subroom_2 = (wall_x + 1, y, w - (wall_x - x) - 1, h)
        return [new_subroom_1, new_subroom_2]

    def split_subroom_horizontally(self, x, y, w, h):
        wall_y = random.randint(y + self.min_subroom_dimension, y + h - 1 - self.min_subroom_dimension)

        wall_start_x = x
        wall_end_x = x + w - 1

        for wall_x in range(wall_start_x, wall_end_x + 1):
            self.room_map[wall_y][wall_x] = WALL_CHARACTER

        door_generated = False

        if self.room_map[wall_y][wall_start_x - 1] == EMPTY_CHARACTER:
            self.room_map[wall_y][wall_start_x] = EMPTY_CHARACTER
            door_generated = True

        if self.room_map[wall_y][wall_end_x + 1] == EMPTY_CHARACTER:
            self.room_map[wall_y][wall_end_x] = EMPTY_CHARACTER
            door_generated = True

        if not door_generated:
            self.room_map[wall_y][random.randint(wall_start_x, wall_end_x)] = EMPTY_CHARACTER

        new_subroom_1 = (x, y, w, wall_y - y)
        new_subroom_2 = (x, wall_y + 1, w, h - (wall_y - y) - 1)
        return [new_subroom_1, new_subroom_2]

    def generate_subrooms(self):
        subrooms = []

        # (top left x, top left y, width, height)
        subroom_stack = [(1, 1, self.width - 2, self.height - 2)]

        while len(subroom_stack) != 0:
            x, y, w, h = subroom = subroom_stack.pop()

            possible_wall_directions = []

            if w >= self.min_splittable_subroom_dimension:
                possible_wall_directions.append(WALL_VERTICAL)

            if h >= self.min_splittable_subroom_dimension:
                possible_wall_directions.append(WALL_HORIZONTAL)

            if len(possible_wall_directions) == 0:
                subrooms.append(subroom)
                continue

            if random.choice(possible_wall_directions) == WALL_VERTICAL:
                subroom_stack.extend(self.split_subroom_vertically(*subroom))
            else:
                subroom_stack.extend(self.split_subroom_horizontally(*subroom))

        return subrooms

    def generate_interior(self, subroom_count):
        monster_count = subroom_count // 2
        monster_order = [ZOMBIE_CHARACTER, ZOMBIE_CHARACTER, VAMPIRE_CHARACTER, ZOMBIE_CHARACTER,
                        HUNTER_CHARACTER, VAMPIRE_CHARACTER]
        for i, char in zip(range(monster_count), cycle(monster_order)):
            x, y = self.find_random_unused_position()
            self.room_map[y][x] = char

        for char in [FOG_CHARACTER, SPEED_CHARACTER]:
            x, y = self.find_random_unused_position()
            self.room_map[y][x] = char

    def find_random_unused_position(self):
        x, y = 0, 0
        while self.room_map[y][x] != EMPTY_CHARACTER:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        return x, y

    def generate_exit_position(self, start_x, start_y):
        """
        At distant a place from start.
        """
        distance_map = [[-1 for x in range(self.width)] for y in range(self.height)]

        q = Queue()
        q.put((start_x, start_y))
        distance_map[start_y][start_x] = 0

        exit_x, exit_y = 0, 0

        while not q.empty():
            exit_x, exit_y = x, y = q.get()
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self.room_map[ny][nx] == EMPTY_CHARACTER and distance_map[ny][nx] == -1:
                    distance_map[ny][nx] = distance_map[y][x] + 1
                    q.put((nx, ny))

        self.room_map[exit_y][exit_x] = EXIT_CHARACTER

    def generate_random_room(self):
        """
        Creates a 2D map of characters.
        """

        self.set_up_empty_room_with_sentinels()

        subrooms = self.generate_subrooms()

        start_x, start_y = self.find_random_unused_position()
        self.room_map[start_y][start_x] = START_CHARACTER

        self.generate_exit_position(start_x, start_y)

        self.generate_interior(len(subrooms))


def save_map(room_map, filename):
    with open(filename, "w") as file:
        file.write("\n".join(map("".join, room_map)))
