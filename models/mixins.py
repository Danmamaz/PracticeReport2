from random import choice


class CMS:
    location_i = 1
    round_counter = 1
    turn_counter = 0
    i = 0
    location = None
    player_buttons = None
    enemy = None
    enemy_hpb = None
    player = None
    player_hpb = None
    info_label = None
    color = None
    image_enemy = None
    image_player = None
    money_label = None
    skip_turn = False
    location_label = None
    run_info = None
    counter = None
    bg_color = None
    sprite = None
    sprites = [("Images/Tree.png", (50, 200)),("Images/Tree.png", (550, 70)),("Images/Tree.png", (500, 300))]
    c_sprites = []

    b_upgrade = None
    w_upgrade = None
    s_upgrade = None
    diamonds = 0

    @staticmethod
    def block_buttons():
        for button in CMS.player_buttons:
            button.unbind("<Button-1>")
            button.configure(state="disabled", fg_color="black")

    def toggle_moves(self):
        if CMS.enemy.dead:
            self.progress_location()
        elif CMS.player.dead:
            self.death_screen()
            CMS.location_i = 1
            CMS.round_counter = 1
        else:
            CMS.turn_counter += 1
            self.block_buttons()

            if (CMS.turn_counter - 1) % 2 == 0:
                if not CMS.skip_turn:
                    self.player_move()
                    CMS.color = "green"
                else:
                    self.ai_move()
                    CMS.color = "red"
                    CMS.skip_turn = False
            else:
                self.ai_move()
                CMS.color = "red"

    def player_move(self):
        for button in self.player_buttons:
            button.bind("<Button-1>", lambda e: self.toggle_moves())
            button.configure(state="normal", fg_color="#343645")

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
        if CMS.location_i == 4:
            self.init_win()
            CMS.diamonds += 1
            CMS.location_i = 1
            CMS.round_counter = 1
            CMS.refresh_diamond_counter()
            return
        CMS.turn_counter = 0
        CMS.round_counter += 1

        if not CMS.round_counter == 5 and not CMS.round_counter == 6:
            CMS.player.money += CMS.enemy.money

        if CMS.round_counter == 4:
            self.init_shop()
        elif CMS.round_counter == 5:
            self.init_fight(CMS.player, CMS.location.boss_encounter())
        elif CMS.round_counter == 6:
            CMS.round_counter = 0
            CMS.location_i += 1
            self.new_location("cave" if CMS.location_i == 2 else "water")
        else:
            self.init_fight(CMS.player, CMS.location.enemy_encounter())

    @staticmethod
    def refresh_diamond_counter():
        CMS.counter.configure(text=f"Diamonds\n{CMS.diamonds}")
