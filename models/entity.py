from models.mixins import *


class Entity(CrossModuleSupport):
    def __init__(self, health: int, armor: int, damage_range: tuple, image: str):
        self.dead = False
        self.health = health
        self.max_health = health
        self.armor = armor
        self.damage = range(*damage_range)
        self.heal_amount = self.health * 20/100
        self.defend_counter = 0
        self.options = [self.attack, self.defend, self.unique_option]
        self.image = image
        self.money = 0

    def attack(self, target, target_health_bar):
        target.take_damage(choice(self.damage))
        target_health_bar.set((target.health * target.max_health / 100) / 100)
        return "Attacked!"

    def defend(self):
        self.defend_counter += 1
        return f"You have {self.defend_counter} damage blocks!"

    def unique_option(self):
        pass

    def take_damage(self, amount: int):
        if self.defend_counter:
            self.defend_counter -= 1
            return "Damage blocked!"
        self.health -= amount
        if self.health <= 0:
            self.dead = True
        return f"-{amount} health"

    def __str__(self):
        return (f"Health: {self.health}\n"
                f"Armor: {self.armor}\n"
                f"Defend counter: {self.defend_counter}\n")

    def give_item(self, item):
        pass


class Warrior(Entity):
    def __init__(self, health: int = 100, armor: int = 20, damage_range: tuple = (10,20), image: str = ""):
        super().__init__(health, armor, damage_range, image)
        self.options = [self.attack, self.defend, self.buff]
        self.option_buttons = None
        self.buff_counts = 0
        self.buff_mult = 2
        self.unique_option_name = "Buff"


    def buff(self):
        self.buff_counts += 1
        return f"Next attack will deal {self.buff_mult}x damage"

    def attack(self, target, target_health_bar):
        if self.buff_counts != 0:
            damage_amount = choice(self.damage) * self.buff_mult
            self.buff_counts -= 1
        else:
            damage_amount = choice(self.damage)
        target.take_damage(damage_amount)
        target_health_bar.set(target.health / target.max_health)
        return "Attacked!"

    def defend(self):
        super().defend()
        self.block_buttons()


class Enemy(Entity):
    def __init__(self, health: int, armor: int, damage_range: tuple, image: str, money: int):
        super().__init__(health, armor, damage_range, image)
        self.money = money

