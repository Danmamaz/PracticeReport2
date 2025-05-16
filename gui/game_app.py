import customtkinter as ctk
from models.entity import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("Game")
        self.resizable(False, False)
        self.tabview = None
        self.start_button = None
        self.player_buttons = []
        self.round_counter = 0
        ctk.set_appearance_mode("light")

        self.create_ui()

    def create_ui(self):
        # Creating main UI component
        self.tabview = VerticalTabView(self, {"Fight": None, "Store": None, "Tutorial": None})
        self.tabview.pack(expand=True, fill="both")

        # Buttons for game and tutorial
        self.start_button = ctk.CTkButton(self.tabview.tabs["Fight"], text="Start new run",
                                          command=self.init_fight)
        self.start_button.pack()

    def init_fight(self, player=Warrior(100, 0, (24, 30)),
                        enemy=Entity(100, 0, (24, 30))):

        # forgetting old button and create point variable for objects to pack
        self.start_button.pack_forget()
        land = self.tabview.tabs["Fight"]

        # Enemy UI
        enemy_name_l = ctk.CTkLabel(land, text="Enemy name")
        enemy_name_l.pack(padx=10)

        enemy_sprite = ctk.CTkLabel(land, width=75, height=75, fg_color="gray", text="")
        enemy_sprite.pack()

        enemy_health = ctk.CTkProgressBar(land, mode="determinate")
        enemy_health.set((enemy.health * enemy.max_health / 100) / 100)
        enemy_health.pack()

        # Spacer between enemy and player
        spacer = ctk.CTkLabel(land, height=150, text="")
        spacer.pack()

        # Player UI
        player_sprite = ctk.CTkLabel(land, width=75, height=75, fg_color="gray", text="")
        player_sprite.pack()

        player_health = ctk.CTkProgressBar(land, mode="determinate")
        player_health.set((player.health * player.max_health / 100) / 100)
        player_health.pack()

        player_options = ctk.CTkFrame(land)
        for i, btn in enumerate(["Attack", "Defend", f"{player.unique_option_name}"]):
            option = ctk.CTkButton(player_options, text=btn, width=80, height=30, state="disabled",
                                   command=player.options[i] if i != 0 else lambda t=enemy, hpb=enemy_health: player.attack(t, hpb))
            option.pack(pady=15, side="left")
            self.player_buttons.append(option)

        player_options.pack()

    def toggle_moves(self):
        if self.round_counter % 2 == 0:
            player_move()
        else:
            ai_move()
        self.round_counter += 1

    def player_move(self):
        for button in self.player_buttons:
            button.configure(state="normal")
        self.round_counter += 1

    def ai_move(self):


class VerticalTabView(ctk.CTkFrame):
    def __init__(self, master, tabs):
        super().__init__(master)

        self.tabs = {}
        self.buttons = []
        self.current_tab = None
        self.current_button = None

        self.left_frame = ctk.CTkFrame(self, width=200)
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="left", fill="both", expand=True)

        for name in tabs:
            btn = ctk.CTkButton(self.left_frame, text=name, width=150, height=40)
            btn.configure(command=lambda b=btn, n=name: self.switch_tab(n, b))
            btn.pack(pady=10)

            frame = ctk.CTkFrame(self.right_frame)
            self.tabs[name] = frame
            self.buttons.append(btn)

        self.switch_tab(list(tabs.keys())[0], self.buttons[0])

    def switch_tab(self, name, btn):
        if self.current_tab:
            self.tabs[self.current_tab].pack_forget()
        self.tabs[name].pack(fill="both", expand=True)
        self.current_tab = name

        for button in self.buttons:
            button.configure(fg_color="transparent")
        btn.configure(fg_color="green")
        self.current_button = btn
