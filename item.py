from thing import Thing

class Item(Thing):
    def use(self, player):
        pass


class SpeedBoost(Item):
    def use(self, player):
        player.speed = 2


class Fog(Item):
    def use(self, player):
        player.vision = 5
