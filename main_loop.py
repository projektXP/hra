import pygame
from room import Room
from thing import Thing
from monster import Monster


pygame.init()


r = Room(32)
r.load_from_file("level.map")

screen = pygame.display.set_mode(r.canvas_size())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for monster in r.things_of_class(Monster, static_map=False):
        monster.step()

    r.player.step()

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
