from models.mixins import *


class Entity(CMS):
    def __init__(self, health: int, armor: int, damage_range: tuple, image: str):
        self.dead = False
        self.health = health
        self.max_health = health
        self.armor = armor
        self.damage = range(*damage_range)
        self.heal_amount = self.max_health * 20/100
        self.defend_counter = 0
        self.options = [self.attack, self.defend]
        self.image = image
        self.money = 0

    def attack(self, target, target_health_bar):
        target.take_damage(choice(self.damage))
        target_health_bar.set((target.health * target.max_health / 100) / 100)
        CMS.info_label.configure(text="Attacked!", text_color=CMS.color)

    def defend(self):
        self.defend_counter += 1
        CMS.info_label.configure(text=f"{self.defend_counter} damage blocks!", text_color=CMS.color)

    def take_damage(self, amount: int):
        if self.defend_counter:
            self.defend_counter -= 1
            CMS.info_label.configure(text="Damage blocked!", text_color=CMS.color)
            return
        self.health -= amount
        if self.health <= 0:
            self.dead = True
        CMS.info_label.configure(text=f"-{amount} health", text_color=CMS.color)


class Warrior(Entity):
    def __init__(self, health: int = 100, armor: int = 20, damage_range: tuple = (100, 200), image: str = ""):
        super().__init__(health, armor, damage_range, image)
        self.options = [self.attack, self.defend, self.buff]
        self.buff_counts = 0
        self.buff_mult = 2 if not CMS.w_upgrade else 3
        self.unique_option_name = "Buff"

    def buff(self):
        self.buff_counts += 1
        CMS.info_label.configure(text=f"Next attack will deal {self.buff_mult}x damage", text_color=CMS.color)

    def attack(self, target, target_health_bar):
        if self.buff_counts != 0:
            damage_amount = choice(self.damage) * self.buff_mult
            self.buff_counts -= 1
        else:
            damage_amount = choice(self.damage)
        target.take_damage(damage_amount)
        target_health_bar.set(target.health / target.max_health)
        CMS.info_label.configure(text="Attacked!", text_color=CMS.color)

    def __str__(self):
        return (f"Health: {self.health}\n"
                f"Armor: {self.armor}\n"
                f"Damage: {self.damage[0]}-{self.damage[-1]}\n"
                f"Ability: {self.unique_option_name}\n"
                f"Next attack \ndealing 2x damage")


class Shaman(Entity):
    def __init__(self, health: int = 100, armor: int = 20, damage_range: tuple = (8, 15), image: str = ""):
        super().__init__(health, armor, damage_range, image)
        self.options = [self.attack, self.heal, self.skadi]
        self.option_buttons = None
        self.buff_counts = 0
        self.buff_mult = 2
        self.unique_option_name = "Skadi"

    @staticmethod
    def skadi():
        try:
            CMS.enemy.options.pop(2)
            CMS.info_label.configure(text=f"Enemy heal ability is removed", text_color=CMS.color)
        except IndexError:
            CMS.info_label.configure(text=f"Enemy heal ability is already removed", text_color=CMS.color)

    def attack(self, target, target_health_bar):
        if self.buff_counts != 0:
            damage_amount = choice(self.damage) * self.buff_mult
            self.buff_counts -= 1
        else:
            damage_amount = choice(self.damage)
        target.take_damage(damage_amount)
        target_health_bar.set(target.health / target.max_health)
        CMS.info_label.configure(text="Attacked!", text_color=CMS.color)

    def heal(self):
        self.health += self.heal_amount if not CMS.s_upgrade else self.max_health - self.health
        CMS.player_hpb.set(self.health / self.max_health)
        if self.health > self.max_health:
            self.health = self.max_health
        CMS.info_label.configure(text=f"Healed", text_color=CMS.color)

    def __str__(self):
        return (f"Health: {self.health}\n"
                f"Armor: {self.armor}\n"
                f"Damage: {self.damage[0]}-{self.damage[-1]}\n"
                f"Ability: {self.unique_option_name}\n"
                f"Removing enemy\nability to heal\n"
                f"'Heal' instead 'Defend'")


class Berserker(Entity):
    def __init__(self, health: int = 120, armor: int = 20, damage_range: tuple = (10, 20), image: str = ""):
        super().__init__(health, armor, damage_range, image)
        self.options = [self.attack, self.defend]
        self.option_buttons = None
        self.buff_counts = 0
        self.buff_mult = 2
        self.unique_option_name = "Rage"

    def attack(self, target, target_health_bar):
        damage_amount = choice(self.damage) + ((self.max_health+1 - self.health) * .1 if not CMS.b_upgrade else .15)
        print(damage_amount)
        target.take_damage(damage_amount)
        target_health_bar.set(target.health / target.max_health)
        CMS.info_label.configure(text="Attacked!", text_color=CMS.color)

    def __str__(self):
        return (f"Health: {self.health}\n"
                f"Armor: {self.armor}\n"
                f"Damage: {self.damage[0]}-{self.damage[-1]}\n"
                f"Ability: {self.unique_option_name}\n"
                f"Passive: More damage\n"
                f"the lower health is")


class Enemy(Entity):
    def __init__(self, health: int, armor: int, damage_range: tuple, image: str, money: int):
        super().__init__(health, armor, damage_range, image)
        self.money = money
        self.options = [self.attack, self.defend, self.heal]

    def heal(self):
        self.health += self.heal_amount
        CMS.enemy_hpb.set(self.health / self.max_health)
        if self.health > self.max_health:
            self.health = self.max_health
        CMS.info_label.configure(text=f"Healed", text_color=CMS.color)

    def __str__(self):
        return self.image


class Boss(Enemy):
    def __init__(self, health: int, armor: int, damage_range: tuple, image: str, money: int, special_move: str):
        super().__init__(health, armor, damage_range, image, money)
        self.thorns_flag = False
        self.options = [self.attack, self.defend, self.heal, eval(f"self.{special_move}")]

    def thorns(self):
        self.thorns_flag = True
        CMS.info_label.configure(text="Taking damage by attacking", text_color=CMS.color)

    @staticmethod
    def ram():
        CMS.skip_turn = True
        CMS.info_label.configure(text="Player skips next 2 turns", text_color=CMS.color)

    def take_damage(self, amount: int):
        if self.defend_counter:
            self.defend_counter -= 1
            CMS.info_label.configure(text="Damage blocked!", text_color=CMS.color)
            return
        self.health -= amount
        if self.thorns_flag:
            CMS.player.take_damage(amount/3)
        if self.health <= 0:
            self.dead = True

    def heal(self):
        self.health += self.heal_amount
        CMS.enemy_hpb.set(self.health / self.max_health)
        if self.health > self.max_health:
            self.health = self.max_health
        CMS.info_label.configure(text=f"Healed", text_color=CMS.color)
