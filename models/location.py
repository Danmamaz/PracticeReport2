from .entity import *
from random import choice


class Location:

    def __init__(self, loc_type):
        self.loc_type = loc_type
        self.stages = 5
        self.stage = 1
        self.enemy_pool_i = 5
        self.location_type = None
        if self.loc_type == "forest":
            self.enemy_pool = [
                Enemy(40, (10, 17), "Bird", 20),
                Enemy(50, (10, 12), "Hedgehog", 10),
                Enemy(35, (15, 22), "Squirrel", 15),
                Enemy(45, (10, 15), "Rabbit", 30),
                Enemy(35, (22, 30), "Mushroom", 0)
               ]
            self.boss = Boss(60, (10, 20), "THE HUNTER", 50, "shotgun")
            CMS.bg_color = "#62bc2f"
            CMS.sprites = [("Images/Tree.png", (50, 200)),("Images/Tree.png", (550, 70)),("Images/Tree.png", (500, 300))]

        elif self.loc_type == "cave":
            self.enemy_pool = [
                Enemy(40, (12, 20), "Snail", 10),
                Enemy(35, (20, 40), "Bat", 15),
                Enemy(50, (17, 25), "Chicken", 25),
                Enemy(40, (15, 16), "Spider", 10),
                Enemy(45, (20, 30), "Rat", 45)
            ]
            CMS.bg_color = "#3A3F4B"
            CMS.sprites = [("Images/Rock.png", (50, 200)),("Images/Rock.png", (550, 70)),("Images/Rock.png", (500, 300))]
            self.boss = Boss(70,  (15, 25), "THE CAVEMAN", 50, "thorns")
        elif self.loc_type == "water":
            self.enemy_pool = [
                Enemy(55, (12, 20), "Puffer Fish", 15),
                Enemy(45, (20, 40), "Sponge Bob", 30),
                Enemy(50, (10, 15), "Shrimp", 15),
                Enemy(62, (20, 25), "Octopus", 20),
                Enemy(55, (15, 30), "Fish", 15)
            ]
            CMS.sprites = [("Images/Bubbles.png", (50, 200)),("Images/Bubbles.png", (550, 70)),("Images/Bubbles.png", (500, 300))]
            CMS.bg_color = "#013A63"
            self.boss = Boss(80, (15, 25), "PRIMORDIAL WYRM", 50, "ram")

    def enemy_encounter(self):
        enemy = self.enemy_pool.pop(choice(range(self.enemy_pool_i)))
        self.enemy_pool_i -= 1
        return enemy

    def boss_encounter(self):
        Location.enemy_pool_i = 5
        return self.boss
