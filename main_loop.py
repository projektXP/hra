import pygame
import os

from room import Room
from thing import Thing
from monster import Monster


class Game:
    def __init__(self):
        self.game_over = False
        self.screen = None
        self.room = None
        self.time = 0

        pygame.init()

        self.room = Room(self, 32)
        self.room.load_from_file(os.path.join("map-files", "level.map"))

        self.screen = pygame.display.set_mode(self.room.canvas_size())
        self.set_game_over_label()

        self.loop()

    def keyboard_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return True
        return False

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            for monster in self.room.things_of_class(Monster, static_map=False):
                monster.step()

            if not self.game_over:
                self.room.player.step()
                self.room.update_tracking()
            elif self.keyboard_quit():
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

            if self.game_over:
                self.print_game_over()

            pygame.display.flip()
            pygame.time.wait(15)

            self.time += 1

    def set_game_over_label(self):
        font_path = os.path.join("fonts", "youmurdererbb_reg.ttf")
        font = pygame.font.Font(font_path, 100)

        self.game_over_label = font.render("Game Over!", 0, (200, 0, 0))

        self.game_over_x, self.game_over_y = self.room.canvas_size()
        self.game_over_x //= 2
        self.game_over_y //= 2
        self.game_over_x -= self.game_over_label.get_width() // 2
        self.game_over_y -= self.game_over_label.get_height() // 2

    def print_game_over(self):
        self.screen.blit(self.game_over_label, (self.game_over_x, self.game_over_y))

game = Game()
