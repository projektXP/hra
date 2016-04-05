from thing import Thing
import pygame


class Player(Thing):
    def __init__(self, room, x=0, y=0):
        super().__init__(room, x, y)
        self.canvas.fill((255, 0, 0))
        self.movements = {
            pygame.K_LEFT:  (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP:    (0, -1),
            pygame.K_DOWN:  (0, 1),
        }

        self.vision = 3

    def move(self):
        keys = pygame.key.get_pressed()
        for key in self.movements:
            if keys[key]:
                self.move_to(self.x + self.movements[key][0], self.y + self.movements[key][1])
