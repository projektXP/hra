import unittest
import os
from room import Room


class RoomLoadFromFileTests(unittest.TestCase):
    def test_invalid_filename(self):
        room = Room(20)
        with self.assertRaises(FileNotFoundError):
            room.load_from_file("gibberish")

    def test_jagged_lines(self):
        room = Room(20)
        with self.assertRaisesRegex(RuntimeError, "invalid input file: jagged lines"):
            room.load_from_file(os.path.join("test-files", "jagged.map"))

    def test_all_characters(self):
        room = Room(20)
        room.load_from_file(os.path.join("test-files", "all-characters.map"))

    def test_invalid_character(self):
        room = Room(20)
        with self.assertRaisesRegex(RuntimeError, "invalid input file: character '.' not mapped to any object"):
            room.load_from_file(os.path.join("test-files", "invalid-character.map"))

    def test_no_player(self):
        room = Room(20)
        with self.assertRaisesRegex(RuntimeError, "no player present in room"):
            room.load_from_file(os.path.join("test-files", "no-player.map"))

    def test_more_players(self):
        room = Room(20)
        with self.assertRaisesRegex(RuntimeError, "player already present in room"):
            room.load_from_file(os.path.join("test-files", "more-players.map"))

    def test_empty(self):
        room = Room(20)
        with self.assertRaisesRegex(RuntimeError, "no player present in room"):
            room.load_from_file(os.path.join("test-files", "empty.map"))


class RoomCanMoveToTests(unittest.TestCase):
    def test_move_out_of_bounds(self):
        room = Room(20)
        room.load_from_file(os.path.join("test-files", "boundaries-test.map"))
        self.assertEqual(room.width, 10)
        self.assertEqual(room.height, 6)

        self.assertFalse(room.can_move_to(-1, 0))
        self.assertFalse(room.can_move_to(10, 0))
        self.assertFalse(room.can_move_to(0, -1))
        self.assertFalse(room.can_move_to(0, 6))


if __name__ == '__main__':
    unittest.main()
