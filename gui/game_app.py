import customtkinter as ctk
from models.location import *


class App(ctk.CTk, CMS):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("Game")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        self.selected_char = None

        self.tabview = None
        self.start_button = None
        self.player_buttons = []

        self.create_ui()

    def create_ui(self):
        # Creating main UI component
        self.tabview = VerticalTabView(self, {"Fight": None, "Store": None, "Tutorial": None})
        self.tabview.pack(expand=True, fill="both")

        # Buttons for game and tutorial
        heading = ctk.CTkLabel(self.tabview.tabs["Fight"], text="Select character")
        heading.pack()

        self.characters_f = ctk.CTkFrame(self.tabview.tabs["Fight"])
        for i, char in enumerate(["Warrior", "Char 2", "Char 3"]):
            frame = ctk.CTkFrame(self.characters_f)
            heading = ctk.CTkLabel(frame, text=f"{char}")
            img_box = ctk.CTkLabel(frame, text="", fg_color="gray", width=100, height=100)
            button = ctk.CTkButton(frame, text=f"Pick {i}", command=lambda c=char: self.select_character(c))
            heading.pack()
            img_box.pack()
            button.pack()
            frame.pack(side="left")

        self.characters_f.pack()

        self.start_button = ctk.CTkButton(self.tabview.tabs["Fight"], text="Start new run",
                                          command=self.init_run)
        self.start_button.pack()

    def select_character(self, name):
        self.selected_char = eval(f"{name}()")

    def init_run(self):
        if self.selected_char:
            location = Location("forest")
            CMS.location = location
            self.init_fight(self.selected_char, location.enemy_encounter())

        else:
            self.heading.configure(text="You cant start a run\nif you not picked character")

    def init_shop(self):
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()
        land = self.tabview.tabs["Fight"]

        heading = ctk.CTkLabel(land, text="Shop")
        heading.pack()

        items_frame = ctk.CTkFrame(land)
        items_frame.pack()
        for i in ["Item 1", "Item 2", "Item 3"]:
            frame = ctk.CTkFrame(items_frame)
            image = ctk.CTkLabel(frame, text="", width=75, height=75, fg_color="gray")
            button = ctk.CTkButton(frame, text="Buy", command=None)

            frame.pack(side="left")
            image.pack()
            button.pack()

        button = ctk.CTkButton(land, text="Leave", command=lambda: self.toggle_moves())
        button.pack()

    @staticmethod
    def new_location(l_type):
        new_location = Location(l_type)
        CMS.location = new_location

    def init_fight(self, player, enemy):
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()
        land = self.tabview.tabs["Fight"]

        # Enemy UI
        enemy_name_l = ctk.CTkLabel(land, text=f"{enemy.image}")
        enemy_name_l.pack(padx=10)

        enemy_sprite = ctk.CTkLabel(land, width=75, height=75, fg_color="gray", text="")
        enemy_sprite.pack()

        enemy_health = ctk.CTkProgressBar(land, mode="determinate")
        enemy_health.set(1)
        CMS.enemy_hpb = enemy_health
        enemy_health.pack()

        # Info between enemy and player
        info_l = ctk.CTkLabel(land, height=150, text="")
        info_l.pack()

        # Player UI
        player_sprite = ctk.CTkLabel(land, width=75, height=75, fg_color="gray", text="")
        player_sprite.pack()

        player_health = ctk.CTkProgressBar(land, mode="determinate")
        player_health.set((player.health * player.max_health / 100) / 100)
        player_health.pack()

        player_options = ctk.CTkFrame(land)
        for i, btn in enumerate(["Attack", "Defend", f"{player.unique_option_name}"]):
            option = ctk.CTkButton(player_options, text=btn, width=80, height=30, state="disabled",
                                   command=player.options[i] if i != 0 else lambda: player.attack(enemy, enemy_health))
            option.pack(pady=15, side="left")
            option.bind("<Button-1>", lambda e: self.toggle_moves())
            self.player_buttons.append(option)

        player.option_buttons = CMS.player_buttons = self.player_buttons
        CMS.enemy = enemy
        CMS.player = player
        CMS.player_hpb = player_health

        player_options.pack()
        self.toggle_moves()


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
