"""
1) Generate sub-rooms
    - select sub-room
    - create wall in sub-room with entrance
    - add 2 new sub-rooms to list

2) Generate interiors of sub-rooms
    - monsters, items
    - non-blocking walls

3) Put start at random place

4) Put exit at place that is far enough
"""

import random

MIN_SUBROOM_DIMENSION = 4
MIN_SPLITTABLE_SUBROOM_DIMENSION = 2 * MIN_SUBROOM_DIMENSION + 1
WALL_VERTICAL = 0
WALL_HORIZONTAL = 1

WALL_CHARACTER = "#"
EMPTY_CHARACTER = "."
START_CHARACTER = "S"


def split_subroom_vertically(room_map, x, y, w, h):
    wall_x = random.randint(x + MIN_SUBROOM_DIMENSION, x + w - 1 - MIN_SUBROOM_DIMENSION)

    wall_start_y = y
    wall_end_y = y + h - 1

    for wall_y in range(wall_start_y, wall_end_y + 1):
        room_map[wall_y][wall_x] = "#"

    door_generated = False

    if room_map[wall_start_y - 1][wall_x] == EMPTY_CHARACTER:
        room_map[wall_start_y][wall_x] = EMPTY_CHARACTER
        door_generated = True

    if room_map[wall_end_y + 1][wall_x] == EMPTY_CHARACTER:
        room_map[wall_end_y][wall_x] = EMPTY_CHARACTER
        door_generated = True

    if not door_generated:
        room_map[random.randint(wall_start_y, wall_end_y)][wall_x] = EMPTY_CHARACTER

    new_subroom_1 = (x, y, wall_x - x, h)
    new_subroom_2 = (wall_x + 1, y, w - (wall_x - x) - 1, h)
    return [new_subroom_1, new_subroom_2]


def split_subroom_horizontally(room_map, x, y, w, h):
    wall_y = random.randint(y + MIN_SUBROOM_DIMENSION, y + h - 1 - MIN_SUBROOM_DIMENSION)

    wall_start_x = x
    wall_end_x = x + w - 1

    for wall_x in range(wall_start_x, wall_end_x + 1):
        room_map[wall_y][wall_x] = WALL_CHARACTER

    door_generated = False

    if room_map[wall_y][wall_start_x - 1] == EMPTY_CHARACTER:
        room_map[wall_y][wall_start_x] = EMPTY_CHARACTER
        door_generated = True

    if room_map[wall_y][wall_end_x + 1] == EMPTY_CHARACTER:
        room_map[wall_y][wall_end_x] = EMPTY_CHARACTER
        door_generated = True

    if not door_generated:
        room_map[wall_y][random.randint(wall_start_x, wall_end_x)] = EMPTY_CHARACTER

    new_subroom_1 = (x, y, w, wall_y - y)
    new_subroom_2 = (x, wall_y + 1, w, h - (wall_y - y) - 1)
    return [new_subroom_1, new_subroom_2]


def generate_subrooms(room_map, w, h):
    subrooms = []

    # (top left x, y, width, height)
    subroom_stack = [(1, 1, w - 2, h - 2)]

    while len(subroom_stack) != 0:
        x, y, w, h = subroom = subroom_stack.pop()

        possible_wall_directions = []

        if w >= MIN_SPLITTABLE_SUBROOM_DIMENSION:
            possible_wall_directions.append(WALL_VERTICAL)

        if h >= MIN_SPLITTABLE_SUBROOM_DIMENSION:
            possible_wall_directions.append(WALL_HORIZONTAL)

        if len(possible_wall_directions) == 0:
            subrooms.append(subroom)
            continue

        if random.choice(possible_wall_directions) == WALL_VERTICAL:
            subroom_stack.extend(split_subroom_vertically(room_map, *subroom))
        else:
            subroom_stack.extend(split_subroom_horizontally(room_map, *subroom))

    return subrooms


def generate_interior(room_map, x, y, w, h):
    pass


def find_suitable_start_position(room_map, width, height):
    x, y = 0, 0
    while room_map[y][x] != EMPTY_CHARACTER:
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    return x, y


def find_suitable_exit_position(room_map):
    pass


def generate_random_room():
    """
    Creates a 2D map of characters.
    """
    width, height = 20, 20

    room_map = [[WALL_CHARACTER for x in range(width)] for y in range(height)]

    for y in range(1, height-1):
        for x in range(1, width-1):
            room_map[y][x] = EMPTY_CHARACTER

    subrooms = generate_subrooms(room_map, width, height)

    for subroom in subrooms:
        generate_interior(room_map, *subroom)

    start_x, start_y = find_suitable_start_position(room_map, width, height)
    room_map[start_y][start_x] = START_CHARACTER

    return room_map


def save_map(room_map, filename):
    with open(filename, "w") as file:
        file.write("\n".join(map("".join, room_map)))

random.seed()
save_map(generate_random_room(), "generated.map")
