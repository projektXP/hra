import pygame

from room import Room
from thing import Thing
from monster import Monster, Hunter, Zombie, Vampire
from player import Player

pygame.init()

r = Room(20, 40, 30)
p = Player(r, 1, 1)
Hunter(r, 39, 29, p)
Zombie(r, 0, 29, p)
Vampire(r, 20, 29, p)
Hunter(r, 39, 10, p)
Zombie(r, 0, 10, p)
Vampire(r, 20, 10, p)

screen = pygame.display.set_mode(r.canvas_size())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for monster in r.things_of_class(Monster):
        monster.step()

    p.move()

    screen.fill((255, 255, 255))

    for thing in r.things_of_class(Thing):
        img = thing.draw()
        screen.blit(img, r.abs_coords(thing.x, thing.y))

    pygame.display.flip()
    pygame.time.wait(50)
