from random import choice
from .mixins import *


class Item:
    def __init__(self):
        self.effect, self.cost, self.name = choice([(self.heal_small, 20, "Small Healing Potion"),
                                                    (self.heal_medium, 30, "Medium Healing Potion"),
                                                    (self.heal_big, 40, "Big Healing Potion"),
                                                    (self.upgrade_attack, 100, "2X Damage upgrade")])

    def heal_small(self):
        print(CMS.player.money)
        if self.buy_item():
            CMS.player.health += CMS.player.max_health / 3
            CMS.player.health = CMS.player.health if CMS.player.health < CMS.player.max_health else CMS.player.max_health
            print(CMS.player.money)

    def heal_medium(self):
        print(CMS.player.money)
        if self.buy_item():
            CMS.player.health += CMS.player.max_health / 2
            CMS.player.health = CMS.player.health if CMS.player.health < CMS.player.max_health else CMS.player.max_health
            print(CMS.player.money)

    def heal_big(self):
        print(CMS.player.money)
        if self.buy_item():
            CMS.player.health += CMS.player.max_health
            print(CMS.player.money)
            CMS.player.health = CMS.player.health if CMS.player.health < CMS.player.max_health else CMS.player.max_health

    def upgrade_attack(self):
        if self.buy_item():
            CMS.player.damage_range = tuple([item * 2 for item in CMS.player.damage_range])

    def buy_item(self):
        if CMS.player.money > self.cost:
            CMS.player.money -= self.cost
            self.cost *= 1.5
            return True
        return False

    def __str__(self):
        return (f"{self.name}\n"
                f"{self.cost} gold")
