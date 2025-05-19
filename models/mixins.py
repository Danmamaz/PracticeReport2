from random import choice


class CMS:
    location_i = 1
    round_counter = 0
    turn_counter = 0
    location = None
    player_buttons = None
    enemy = None
    enemy_hpb = None
    player = None
    player_hpb = None

    @staticmethod
    def block_buttons():
        for button in CMS.player_buttons:
            button.unbind("<Button-1>")
            button.configure(state="disabled")

    def toggle_moves(self):
        if CMS.enemy.dead:
            self.progress_location()

        else:
            CMS.turn_counter += 1
            self.block_buttons()
            return self.player_move() if (CMS.turn_counter - 1) % 2 == 0 else self.ai_move()

    def player_move(self):
        for button in self.player_buttons:
            button.bind("<Button-1>", lambda e: self.toggle_moves())
            button.configure(state="normal")

    def ai_move(self):

        def move():
            option = choice(CMS.enemy.options)
            if option == CMS.enemy.attack:
                option(CMS.player, CMS.player_hpb)
            else:
                option()
            self.toggle_moves()

        self.after(1000, move)

    def progress_location(self):
        CMS.player.money += CMS.enemy.money
        CMS.turn_counter = 0
        CMS.round_counter += 1

        if CMS.round_counter == 4:
            self.init_shop()
            CMS.round_counter += 1
        elif CMS.round_counter == 5:
            self.init_fight(CMS.player, CMS.location.boss_encounter())
        elif CMS.round_counter == 6:
            CMS.round_counter = 0
            CMS.location_i += 1
            self.new_location("cave" if CMS.location_i == 2 else "water")
        else:
            self.init_fight(CMS.player, CMS.location.enemy_encounter())

