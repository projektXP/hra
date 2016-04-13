import pygame
from thing import Thing

class Wall(Thing):
    def __init__(self, room, x, y, nameOfPic='wall'):
        super().__init__(room,x,y)
        self._address = self._retPicture(nameOfPic)
        self.drawPic()

    def _retPicture(self,name) -> str:
        if name in self.dictOfPic:
            return self.dictOfPic[name]
        return ""

    def drawPic(self):
        if self._address:
            image = pygame.image.load(self._address)
            self.canvas.blit(image,(0,0))

