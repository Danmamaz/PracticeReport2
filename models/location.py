from .entity import *
from random import choice


class Location:
    def __init__(self, loc_type):
        self.loc_type = loc_type
        self.stages = 5
        self.stage = 1
        self.location_type = None
        if self.loc_type == "forest":
            self.enemy_pool = [
                Enemy(30, 10, (10, 17), "Bird", 20),
                Enemy(40, 20, (10, 12), "Hedgehog", 10),
                Enemy(25, 12, (15, 22), "Squirrel", 15),
                Enemy(35, 5, (10, 15), "Rabbit", 30),
                Enemy(25, 1, (22, 30), "Mushroom", 0)
               ]
            self.boss = Boss(100, 30, (20, 30), "NIGGA", 50, "thorns")
        elif self.loc_type == "cave":
            self.enemy_pool = [
                Enemy(20, 40, (12, 20), "Snail", 10),
                Enemy(15, 10, (20, 40), "Bat", 15),
                Enemy(30, 15, (17, 25), "Chicken", 25),
                Enemy(20, 20, (15, 16), "Spider", 10),
                Enemy(25, 10, (20, 30), "Rat", 45)
            ]

        elif self.loc_type == "water":
            self.enemy_pool = [
                Enemy(25, 10, (12, 20), "PufferFish", 15),
                Enemy(55, 20, (20, 40), "SpongeBob", 30),
                Enemy(20, 10, (10, 15), "Shrimp", 15),
                Enemy(32, 15, (20, 25), "Octopus", 20),
                Enemy(25, 10, (15, 30), "Fish", 15)
            ]

    def enemy_encounter(self):
        enemy = choice(self.enemy_pool)
        return enemy

    def store_section(self):
        pass

    def boss_encounter(self):
        return self.boss
