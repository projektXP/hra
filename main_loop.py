import pygame

from room import Room
from thing import Thing
from monster import Monster, Hunter, Zombie, Vampire


pygame.init()

r = Room(20)
r.load_from_file("level.map")

Hunter(r, 39, 29)
Zombie(r, 0, 29)
Vampire(r, 20, 29)
Hunter(r, 39, 10)
Zombie(r, 0, 10)
Vampire(r, 20, 10)


screen = pygame.display.set_mode(r.canvas_size())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for monster in r.things_of_class(Monster):
        monster.step()

    r.player.move()

    screen.fill((255, 255, 255))

    for thing in r.things_of_class(Thing):
        img = thing.draw()
        screen.blit(img, r.abs_coords(thing.x, thing.y))

    pygame.display.flip()
    pygame.time.wait(50)
