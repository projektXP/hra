import pygame

from room import Room
from thing import Thing
from monster import Monster


class Game:
    def __init__(self):
        self.looping = True
        self.time = 0
        self.loop()
        input()

    def loop(self):
        pygame.init()
        r = Room(self, 32)
        r.load_from_file("level.map")

        screen = pygame.display.set_mode(r.canvas_size())

        while self.looping:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            for monster in r.things_of_class(Monster, static_map=False):
                monster.step()

            r.player.step()
            r.update_tracking()

            screen.fill((127, 127, 127))

            for thing in r.things_of_class(Thing, static_map=True):
                img = thing.draw()
                thing_x, thing_y = thing.get_relative_position_to_draw()
                screen.blit(img, r.abs_coords(thing_x, thing_y))

            for thing in r.things_of_class(Thing, static_map=False):
                img = thing.draw()
                thing_x, thing_y = thing.get_relative_position_to_draw()
                screen.blit(img, r.abs_coords(thing_x, thing_y))

            pygame.display.flip()
            pygame.time.wait(15)

            self.time += 1

game = Game()
