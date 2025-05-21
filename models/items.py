from random import choice
from .mixins import *


class Item:
    def __init__(self):
        self.effect, self.cost, self.name = choice([(self.heal_small, 20, "Small Healing\nPotion"),
                                                    (self.heal_medium, 30, "Medium Healing\nPotion"),
                                                    (self.heal_big, 40, "Big Healing\nPotion"),
                                                    (self.upgrade_attack, 100, "2X Damage\nupgrade")])

    def heal_small(self):
        if self.buy_item():
            CMS.player.health += CMS.player.max_health / 3
            CMS.player.health = CMS.player.health if CMS.player.health < CMS.player.max_health else CMS.player.max_health

    def heal_medium(self):
        if self.buy_item():
            CMS.player.health += CMS.player.max_health / 2
            CMS.player.health = CMS.player.health if CMS.player.health < CMS.player.max_health else CMS.player.max_health

    def heal_big(self):
        if self.buy_item():
            CMS.player.health += CMS.player.max_health
            CMS.player.health = CMS.player.health if CMS.player.health < CMS.player.max_health else CMS.player.max_health

    def upgrade_attack(self):
        if self.buy_item():
            CMS.player.damage_range = tuple([item * 2 for item in CMS.player.damage_range])

    def buy_item(self):
        if CMS.player.money > self.cost:
            CMS.player.money -= self.cost
            print(CMS.player.money)
            self.cost *= 1.5
            CMS.money_label.configure(text=f"Money: {CMS.player.money}")
            CMS.money_label.place(x=10, y=10)
            return True
        return False

    def __str__(self):
        return (f"{self.name}\n"
                f"{self.cost} gold")
