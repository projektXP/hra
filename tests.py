import unittest
from room import Room


class RoomLoadFromFileTests(unittest.TestCase):
    def test_invalid_file(self):
        room = Room(20)
        with self.assertRaises(FileNotFoundError):
            room.load_from_file("gibberish")

if __name__ == '__main__':
    unittest.main()
