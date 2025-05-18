from random import choice

class CrossModuleSupport:
    n_scale = 1
    buttons_enabled = True
    round_counter = 1
    turn_counter = 0
    location = None
    player_buttons = None
    enemy = None
    player = None
    player_hpb = None

    @staticmethod
    def block_buttons():
        CrossModuleSupport.buttons_enabled = False
        [button.configure(state="disabled") for button in CrossModuleSupport.player_buttons]
       
    def toggle_moves(self):
        if CrossModuleSupport.enemy.dead:
            CrossModuleSupport.player.money += CrossModuleSupport.enemy.money
            CrossModuleSupport.turn_counter = 0
            CrossModuleSupport.round_counter += 1
            if CrossModuleSupport.round_counter == 4:
                self.init_shop()
            elif CrossModuleSupport.round_counter == 5:
                print("Boss")
            elif CrossModuleSupport.round_counter == 6:
                CrossModuleSupport.n_scale += 1
                self.new_location(CrossModuleSupport.n_scale, "cave" if CrossModuleSupport.n_scale == 2 else "water")
            else:
                self.init_fight(CrossModuleSupport.player, CrossModuleSupport.location.enemy_encounter())
        else:
            CrossModuleSupport.turn_counter += 1
            return self.player_move() if (CrossModuleSupport.turn_counter - 1) % 2 == 0 else self.ai_move()



    def player_move(self):
        CrossModuleSupport.buttons_enabled = True
        for button in self.player_buttons:
            button.configure(state="normal")

    def ai_move(self):
        self.block_buttons()
        option = choice(CrossModuleSupport.enemy.options)
        if option == CrossModuleSupport.enemy.attack:
            option(CrossModuleSupport.player, CrossModuleSupport.player_hpb)
        elif option == CrossModuleSupport.enemy.defend:
            option()
        else:
            pass
        self.toggle_moves()
