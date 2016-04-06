import pygame

from room import Room
from thing import Thing
from monster import Monster, SlowMonster, FastMonster
from player import Player

pygame.init()

r = Room(20, 40, 30)
p = Player(r, 1, 1)
SlowMonster(r, 39, 29, p)

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
