import random as r


class entity:
    def __init__(self,hp,dmg,armor):
        self.hp = hp
        self.dmg = dmg
        self.armor = armor

    def printHp(self):
        print(self.hp)

class player(entity):
    def __init__(self,hp,dmg,sword):
        super.__init__(hp,dmg)
        self.sword = sword
    def printHp(self):
        super.printHp()

class enemy(entity):
    def __init__():
        pass


entity = entity(25,5)


