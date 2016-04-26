from thing import Thing
from abc import ABCMeta, abstractmethod


class Item(Thing, metaclass=ABCMeta):
    @abstractmethod
    def use(self, player):
        pass


class SpeedBoost(Item):
    def use(self, player):
        player.speed = 2


class Fog(Item):
    def use(self, player):
        player.vision = 5
