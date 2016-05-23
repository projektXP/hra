import unittest
import os

from room import Room
from monster import Vampire
from map_generator import MapGenerator

GRID_SIZE = 32


class RoomLoadFromFileTests(unittest.TestCase):
    def test_invalid_filename(self):
        room = Room(GRID_SIZE)
        with self.assertRaises(FileNotFoundError):
            room.load_from_file("gibberish")

    def test_jagged_lines(self):
        room = Room(GRID_SIZE)
        with self.assertRaisesRegex(RuntimeError, "invalid input file: jagged lines"):
            room.load_from_file(os.path.join("test-files", "jagged.map"))

    def test_all_characters(self):
        room = Room(GRID_SIZE)
        room.load_from_file(os.path.join("test-files", "all-characters.map"))

    def test_invalid_character(self):
        room = Room(GRID_SIZE)
        with self.assertRaisesRegex(RuntimeError, "invalid input file: character '.' not mapped to any object"):
            room.load_from_file(os.path.join("test-files", "invalid-character.map"))

    def test_no_player(self):
        room = Room(GRID_SIZE)
        with self.assertRaisesRegex(RuntimeError, "no starting position present in room"):
            room.load_from_file(os.path.join("test-files", "no-start.map"))

    def test_more_players(self):
        room = Room(GRID_SIZE)
        with self.assertRaisesRegex(RuntimeError, "starting position already present in room"):
            room.load_from_file(os.path.join("test-files", "more-starts.map"))

    def test_empty(self):
        room = Room(GRID_SIZE)
        with self.assertRaisesRegex(RuntimeError, "no starting position present in room"):
            room.load_from_file(os.path.join("test-files", "empty.map"))


class CanMoveToTests(unittest.TestCase):
    def test_player_move_out_of_bounds(self):
        room = Room(GRID_SIZE)
        room.load_from_file(os.path.join("test-files", "boundaries-test.map"))
        self.assertEqual(room.width, 10)
        self.assertEqual(room.height, 6)

        self.assertFalse(room.player.can_move_to(-1, 0))
        self.assertFalse(room.player.can_move_to(10, 0))
        self.assertFalse(room.player.can_move_to(0, -1))
        self.assertFalse(room.player.can_move_to(0, 6))

    def test_monster_move_out_of_bounds(self):
        room = Room(GRID_SIZE)
        room.load_from_file(os.path.join("test-files", "boundaries-test.map"))
        self.assertEqual(room.width, 10)
        self.assertEqual(room.height, 6)
        monster = Vampire(room, 0, 0)

        self.assertFalse(monster.can_move_to(-1, 0))
        self.assertFalse(monster.can_move_to(10, 0))
        self.assertFalse(monster.can_move_to(0, -1))
        self.assertFalse(monster.can_move_to(0, 6))


def count_chars(chars, m):
    count = 0
    for y in range(m.height):
        for x in range(m.width):
            if m.room_map[y][x] in chars:
                count += 1
    return count


class MapGeneratorMethodsTests(unittest.TestCase):
    def test_split_room_horizontally_preserves_dimensions(self):
        m = MapGenerator(3)
        m.set_up_empty_room_with_sentinels()

        room = x, y, w, h = (1, 1, m.width - 2, m.height - 2)

        r1, r2 = m.split_subroom_horizontally(*room)

        self.assertEqual(h, r1[3] + r2[3] + 1)
        self.assertEqual(w, r1[2])
        self.assertEqual(w, r2[2])

    def test_split_room_vertically_preserves_dimensions(self):
        m = MapGenerator(3)
        m.set_up_empty_room_with_sentinels()

        room = x, y, w, h = 1, 1, m.width - 2, m.height - 2

        r1, r2 = m.split_subroom_vertically(*room)

        self.assertEqual(w, r1[2] + r2[2] + 1)
        self.assertEqual(h, r1[3])
        self.assertEqual(h, r2[3])

    def test_generate_subrooms_rooms_large_enough(self):
        min_subroom_dimension = 4

        m = MapGenerator(min_subroom_dimension)
        m.set_up_empty_room_with_sentinels()
        subrooms = m.generate_subrooms()

        for x, y, w, h in subrooms:
            self.assertGreaterEqual(w, min_subroom_dimension)
            self.assertGreaterEqual(h, min_subroom_dimension)

    def test_generate_subrooms_empty_interiors(self):
        m = MapGenerator(4)
        m.set_up_empty_room_with_sentinels()
        subrooms = m.generate_subrooms()

        for x, y, w, h in subrooms:
            for yy in range(y, y + h):
                for xx in range(x, x + w):
                    self.assertEqual(m.room_map[yy][xx], ".")

    def test_generate_subrooms_creates_walls(self):
        m = MapGenerator(4)
        m.set_up_empty_room_with_sentinels()
        subrooms = m.generate_subrooms()

        empty_space_in_rooms = 0
        for x, y, w, h in subrooms:
            empty_space_in_rooms += w*h

        walls = count_chars("#", m)

        empty_space_for_doors = m.width * m.height - walls - empty_space_in_rooms
        max_empty_space_for_doors = (len(subrooms) - 1) * 2
        min_empty_space_for_doors = len(subrooms) - 1

        self.assertGreaterEqual(empty_space_for_doors, min_empty_space_for_doors)
        self.assertGreaterEqual(max_empty_space_for_doors, empty_space_for_doors)

    def test_find_random_unused_position(self):
        m = MapGenerator(3)
        m.generate_random_room()
        empty = count_chars(".", m)
        for i in range(empty // 2):
            x, y = m.find_random_unused_position()
            self.assertEqual(m.room_map[y][x], ".")
            m.room_map[y][x] = "#"


class MapGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.m = MapGenerator(3)
        self.m.generate_random_room()

    def test_exactly_one_start(self):
        self.assertEqual(count_chars("S", self.m), 1)

    def test_exactly_one_exit(self):
        self.assertEqual(count_chars("E", self.m), 1)

    def test_all_non_wall_places_reachable(self):
        to_explore = [self.m.find_random_unused_position()]

        while to_explore:
            x, y = to_explore.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
                if self.m.room_map[ny][nx] != "#" and self.m.room_map[ny][nx] != "@":
                    self.m.room_map[ny][nx] = "@"
                    to_explore.append((nx, ny))

        self.assertEqual(count_chars("#@", self.m), self.m.height * self.m.width)


if __name__ == '__main__':
    unittest.main()
