class Entity:
    def __init__(self, health: int, armor: int, damage_range: tuple):
        self.health = health
        self.armor = armor
        self.damage = range(*damage_range)
        self.heal_amount = self.health * 20/100
        self.defend_counter = 0

    def attack(self, target: Entity):
        target.take_damage(self.damage)
        return "Attacked!"

    def defend(self):
        self.defend_counter += 1
        return f"You have {self.defend_counter} damage blocks!"

    def heal(self):
        self.health += self.heal_amount
        return f"You healed by {self.heal_amount} points"

    def take_damage(self, amount: int):
        if self.defend_counter:
            self.defend_counter -= 1
            return "Damage blocked!"
        self.health -= amount * self.armor / 100
        return f"-{amount} health"

    def show_info(self):
        return (f"Health: {self.health}\n"
                f"Armor: {self.armor}\n"
                f"Defend counter: {self.defend_counter}\n")

    def give_item(self, item):
        pass


class Warrior(Entity):
    def __init__(self, health=120, armor=10, damage_range=range(18, 24)):
        super().__init__(health, armor, damage_range)

    def scale_damage(self, scale=1.1):
        self.damage *= scale

