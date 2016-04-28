import unittest
import os
from room import Room
from monster import Vampire

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


if __name__ == '__main__':
    unittest.main()
