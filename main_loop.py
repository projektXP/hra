import pygame
import os

from room import Room
from thing import Thing
from monster import Monster


class Game:
    def __init__(self):
        self.over = False
        self.screen = None
        self.room = None
        self.time = 0
        self.font = None

        self.loop()

    def loop(self):
        pygame.init()
        self.room = Room(self, 32)
        self.room.load_from_file(os.path.join("map-files", "level.map"))

        self.screen = pygame.display.set_mode(self.room.canvas_size())

        font_path = os.path.join("fonts", "youmurdererbb_reg.ttf")
        self.font = pygame.font.Font(font_path, 100)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            for monster in self.room.things_of_class(Monster, static_map=False):
                monster.step()

            if not self.over:
                self.room.player.step()
                self.room.update_tracking()
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                break

            self.screen.fill((127, 127, 127))

            for thing in self.room.things_of_class(Thing, static_map=True):
                img = thing.draw()
                thing_x, thing_y = thing.get_relative_position_to_draw()
                self.screen.blit(img, self.room.abs_coords(thing_x, thing_y))

            for thing in self.room.things_of_class(Thing, static_map=False):
                img = thing.draw()
                thing_x, thing_y = thing.get_relative_position_to_draw()
                self.screen.blit(img, self.room.abs_coords(thing_x, thing_y))

            if self.over:
                game_over = self.font.render("Game Over!", 0, (200, 0, 0))
                game_over_x = self.room.width * self.room.square_size // 2 - game_over.get_width() // 2
                game_over_y = self.room.height * self.room.square_size // 2 - game_over.get_height() // 2
                self.screen.blit(game_over, (game_over_x, game_over_y))

            pygame.display.flip()
            pygame.time.wait(15)

            self.time += 1

game = Game()
