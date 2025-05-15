from random import choice


class Location:
    def __init__(self, difficulty, location_n):
        self.difficulty = difficulty
        self.difficulty_scaling = location_n
        self.stages = 5
        self.stage = 1
        self.location_type = None
        self.enemy_pool = []

    def enemy_encounter(self):
        # enemy = choice(self.enemy_pool)
        pass

    def store_section(self):
        pass

    def boss_encounter(self):
        pass

    def stage_transition(self):
        self.stage += 1
        if self.stage == 3:
            self.store_section()
        elif self.stage == 5:
            self.boss_encounter()
        else:
            self.enemy_encounter()
