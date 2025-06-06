from .mixins import *


class Item:
    def __init__(self):
        self.effect, self.cost, self.name = choice([(self.heal_small, 20, "Small Healing\nPotion"),
                                                    (self.heal_medium, 30, "Medium Healing\nPotion"),
                                                    (self.heal_big, 40, "Big Healing\nPotion"),
                                                    (self.upgrade_attack_3x, 150, "3X Damage\nupgrade"),
                                                    (self.upgrade_attack_2x, 100, "2X Damage\nupgrade"),
                                                    (self.upgrade_attack_half_x, 50, "1.5X Damage\nupgrade"),


                                                    ])

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

    def upgrade_attack_3x(self):
        if self.buy_item():
            CMS.player.damage = range(CMS.player.damage[0] * 3, CMS.player.damage[-1] * 3)

    def upgrade_attack_2x(self):
        if self.buy_item():
            CMS.player.damage = range(CMS.player.damage[0] * 2, CMS.player.damage[-1] * 2)

    def upgrade_attack_half_x(self):
        if self.buy_item():
            CMS.player.damage = range(int(CMS.player.damage[0] * 1.5), int(CMS.player.damage[-1] * 1.5))

    def buy_item(self):
        if CMS.player.money >= self.cost:
            CMS.player.money -= self.cost
            CMS.money_label.configure(text=f"Money: {CMS.player.money}")
            CMS.money_label.pack()
            return True
        return False

    def __str__(self):
        return (f"{self.name}\n"
                f"{self.cost} gold")
