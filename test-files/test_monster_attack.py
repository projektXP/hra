import unittest

class TestMonsterState(unittest.TestCase):

    def test_has_attack_status(self):
        import pygame

        from room import Room
        from thing import Thing
        from monster import Monster


        pygame.init()

        r = Room(20)
        r.load_from_file("../level_attack.map")

        for monster in r.things_of_class(Monster):
            self.assertEqual(monster.state_key, ['think', 'move', 'attack'],'test state_key')
            self.assertEqual(monster.state_val, [True, False, False], 'test state_val')
