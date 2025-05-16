from random import choice


class Entity:
    def __init__(self, health: int, armor: int, damage_range: tuple):
        self.health = health
        self.max_health = health
        self.armor = armor
        self.damage = range(*damage_range)
        self.heal_amount = self.health * 20/100
        self.defend_counter = 0
        self.options = [self.attack, self.defend, self.unique_option]

    def attack(self, target, target_health_bar):
        target.take_damage(self.damage)
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
        return f"-{amount} health"

    def show_info(self):
        return (f"Health: {self.health}\n"
                f"Armor: {self.armor}\n"
                f"Defend counter: {self.defend_counter}\n")

    def give_item(self, item):
        pass


class Warrior(Entity):
    def __init__(self, health: int, armor: int, damage_range: tuple):
        super().__init__(health, armor, damage_range)
        self.options = [self.attack, self.defend, self.buff]
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
        target_health_bar.set((target.health * target.max_health / 100) / 100)
        return "Attacked!"
