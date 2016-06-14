import pygame
import os

from room import Room
from thing import Thing
from monster import Monster
from map_generator import create_random_map_to_file


class Game:
    def __init__(self):
        self.game_over = False
        self.time = 0
        self.room = None
        self.screen = None

        self.overlay = None
        self.overlay_radius = 0

        self.game_over_label = None
        self.game_over_x = 0
        self.game_over_y = 0

    def start(self):
        self.game_over = False
        self.time = 0

        self.room = Room(self, 32)
        self.room.load_from_file(create_random_map_to_file())

        self.screen = pygame.display.set_mode(self.room.canvas_size())
        self.create_overlay()
        self.create_game_over_label()

        self.loop()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if self.game_over and event.type == pygame.KEYDOWN:
                    self.start()

            for monster in self.room.things_of_class(Monster, static_map=False):
                monster.step()

            if not self.game_over:
                self.room.player.step()
                self.room.update_tracking()

            self.screen.fill((127, 127, 127))

            for thing in self.room.things_of_class(Thing, static_map=True):
                img = thing.draw()
                thing_x, thing_y = thing.get_relative_position_to_draw()
                self.screen.blit(img, self.room.abs_coords(thing_x, thing_y))

            for thing in self.room.things_of_class(Thing, static_map=False):
                img = thing.draw()
                thing_x, thing_y = thing.get_relative_position_to_draw()
                self.screen.blit(img, self.room.abs_coords(thing_x, thing_y))

            self.apply_overlay()

            if self.game_over:
                self.print_game_over()

            pygame.display.flip()
            pygame.time.wait(15)

            self.time += 1

    def create_game_over_label(self):
        font_path = os.path.join("fonts", "youmurdererbb_reg.ttf")
        font = pygame.font.Font(font_path, 100)
        self.game_over_label = font.render("Game Over!", 0, (200, 0, 0))

        label_width = self.game_over_label.get_width()
        label_height = self.game_over_label.get_height()
        screen_width, screen_height = self.room.canvas_size()

        self.game_over_x = (screen_width - label_width) // 2
        self.game_over_y = (screen_height - label_height) // 2

    def print_game_over(self):
        self.screen.blit(self.game_over_label, (self.game_over_x, self.game_over_y))

    def create_overlay(self):
        self.overlay_radius = self.room.player.vision * self.room.square_size
        w, h = self.room.canvas_size()
        overlay = pygame.Surface((w * 2, h * 2)).convert_alpha()
        overlay.fill((0, 0, 0, 255))
        pygame.draw.circle(overlay, (0, 0, 0, 0), (w, h), self.overlay_radius)
        self.overlay = overlay

    def apply_overlay(self):
        if self.room.player.vision != self.overlay_radius:
            self.create_overlay()

        half_square = self.room.square_size // 2
        center_x, center_y = self.room.abs_coords(*self.room.player.get_relative_position_to_draw())
        center_x += half_square
        center_y += half_square

        size_x, size_y = self.overlay.get_rect().size
        self.screen.blit(self.overlay, (center_x - size_x // 2, center_y - size_y // 2))


if __name__ == "__main__":
    pygame.init()
    Game().start()
