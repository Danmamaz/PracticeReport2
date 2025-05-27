import customtkinter as ctk
from models.location import *
from PIL import Image
from models.items import *
import json


class App(ctk.CTk, CMS):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.title("Seek Of Adventure")
        self.iconbitmap("Images/Logo.ico")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        self.selected_char = None

        self.my_font = ctk.CTkFont(family="Silkscreen", size=18)
        self.tabview = None
        self.bg_image = None
        self.death_scr = None
        self.start_button = None
        self.player_buttons = []

        self.create_ui()
        self.load_data()
        self.protocol("WM_DELETE_WINDOW", self.save_data)

    def create_ui(self):
        # Creating main UI component
        self.tabview = VerticalTabView(self, {"Fight": None, "Store": None, "Tutorial": None})
        self.tabview.pack(expand=True, fill="both")

        self.fight_ui()
        self.tutorial_ui()
        self.store_ui()

    def fight_ui(self):
        if CMS.c_sprites:
            for item in CMS.c_sprites:
                item.destroy()
            CMS.c_sprites.clear()

        self.tabview.tabs["Fight"].configure(fg_color="gray86")
        # forgetting old widgets and create point variable for objects to pack
        if CMS.run_info:
            CMS.run_info.place_forget()

        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()

        # Buttons for game and tutorial
        self.heading = ctk.CTkLabel(self.tabview.tabs["Fight"], text="Select character", font=("Silkscreen", 30))
        self.heading.pack(pady=(80, 40))

        self.characters_f = ctk.CTkFrame(self.tabview.tabs["Fight"])
        for i, char in enumerate(["Warrior", "Shaman", "Berserker"]):
            frame = ctk.CTkFrame(self.characters_f)
            heading = ctk.CTkLabel(frame, text=f"{char}", font=self.my_font)
            img_box = ctk.CTkLabel(frame, text="", width=100, height=100,
                                   image=ctk.CTkImage(Image.open(f"Images/{char}.png"), size=(100, 100)))
            button = ctk.CTkButton(frame, text=f"Pick",
                                   command=lambda c=char: self.select_character(c), font=self.my_font,
                                   fg_color="#343645", hover_color="#23242E", border_spacing=5)
            heading.pack()
            img_box.pack()
            button.pack(pady=10, padx=10)
            frame.pack(side="left", padx=40, pady=40)

        self.characters_f.pack()

        self.start_button = ctk.CTkButton(self.tabview.tabs["Fight"], text="Start new run",
                                          command=self.init_run, font=("Silkscreen", 24),
                                          fg_color="#343645", border_color="#2E2F33", hover_color="#23242E",
                                          border_spacing=15)
        self.start_button.pack(pady=30)

    def select_character(self, name):
        self.selected_char = eval(f"{name}()")
        self.heading.configure(text=f"Selected: {name}")

    def init_run(self):
        if self.selected_char:
            location = Location("forest")
            CMS.location = location
            CMS.run_info = ctk.CTkFrame(self.tabview.tabs["Fight"], height=200, width=150)
            CMS.run_info.place(x=10, y=10)

            CMS.money_label = ctk.CTkLabel(CMS.run_info, text="", font=self.my_font)
            CMS.money_label.pack(padx=10, pady=5)

            CMS.location_label = ctk.CTkLabel(CMS.run_info, text="", font=("Silkscreen", 18))
            CMS.location_label.pack(padx=10, pady=5)

            self.give_up_l = ctk.CTkButton(CMS.run_info, text="Give Up", command=self.give_up, font=self.my_font,
                                            fg_color="#343645", hover_color="#23242E", border_spacing=5)
            self.give_up_l.pack(padx=10, pady=5)

            self.init_fight(self.selected_char, location.enemy_encounter())

        else:
            self.heading.configure(text="You cant start a run\nif you not picked any character")

    def init_shop(self):
        self.updateable_ui()
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()
        land = self.tabview.tabs["Fight"]

        heading = ctk.CTkLabel(land, text="Shop", font=("Silkscreen", 24))
        heading.pack(pady=(80, 30))

        items_frame = ctk.CTkFrame(land)
        items_frame.pack()
        for item in [Item() for i in range(3)]:
            frame = ctk.CTkFrame(items_frame)
            image = ctk.CTkLabel(frame, text="", width=75, height=75, image=ctk.CTkImage(Image.open("Images/Bag of Money.png"), size=(75, 75)))
            label = ctk.CTkLabel(frame, text=f"{item}", font=self.my_font, wraplength=200)
            button = ctk.CTkButton(frame, text="Buy", command=lambda i=item: i.effect(), font=self.my_font,
                                   fg_color="#343645", hover_color="#23242E", border_spacing=5)

            frame.pack(side="left", padx=20, pady=20)
            image.pack(pady=20)
            label.pack(padx=20)
            button.pack(pady=20, padx=20)

        button = ctk.CTkButton(land, text="Leave", command=lambda: self.toggle_moves(), font=("Silkscreen", 24),
                                          fg_color="#343645", border_color="#2E2F33", hover_color="#23242E",
                                          border_spacing=15)
        button.pack(pady=20)

    @staticmethod
    def updateable_ui():
        CMS.money_label.configure(text=f"Money: {CMS.player.money}")
        CMS.money_label.pack(padx=10)

        CMS.location_label.configure(text=f"Location: {CMS.location.loc_type}")
        CMS.location_label.pack(padx=10)

    def new_location(self, l_type):
        new_location = Location(l_type)
        CMS.location = new_location
        self.progress_location()

    def init_fight(self, player, enemy):
        for item in CMS.c_sprites:
            item.destroy()
        CMS.c_sprites.clear()

        for sprite, cords in CMS.sprites:
            item = ctk.CTkLabel(self.tabview.tabs["Fight"], text="", image=ctk.CTkImage(Image.open(sprite), size=(200, 200)))
            item.place(x=cords[0], y=cords[1])
            CMS.c_sprites.append(item)

        self.tabview.tabs["Fight"].configure(fg_color=CMS.bg_color)
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()
        land = self.tabview.tabs["Fight"]

        CMS.image_enemy = f"Images/{enemy.image}.png"
        CMS.image_player = f"Images/{player.image}.png"

        # Enemy UI
        enemy_box = ctk.CTkFrame(land)
        enemy_name_l = ctk.CTkLabel(enemy_box, text=f"{enemy.image}", font=("Silkscreen", 24))
        enemy_name_l.pack(pady=10)

        enemy_sprite = ctk.CTkLabel(enemy_box, width=125, height=125, fg_color="transparent",
                                    text="", image=ctk.CTkImage(Image.open(CMS.image_enemy), size=(125, 125)),
                                    font=self.my_font)
        enemy_sprite.pack(padx=20)

        enemy_health = ctk.CTkProgressBar(enemy_box, width=enemy.health * 2,
                                          mode="determinate", progress_color="#8C0002")
        enemy_health.set(1)
        CMS.enemy_hpb = enemy_health
        enemy_health.pack(pady=15)
        enemy_box.pack(pady=(40, 10))

        # Info between enemy and player
        info_l = ctk.CTkLabel(land, height=50, text="", font=self.my_font)
        info_l.pack()

        CMS.info_label = info_l

        # Player UI
        player_box = ctk.CTkFrame(land)
        player_sprite = ctk.CTkLabel(player_box, width=125, height=125,
                                     image=ctk.CTkImage(Image.open(CMS.image_player), size=(125, 125)), text="")
        player_sprite.pack(pady=(10, 0))

        player_health = ctk.CTkProgressBar(player_box, width=player.max_health * 2, mode="determinate")
        player_health.set((player.health * player.max_health / 100) / 100)
        player_health.pack(pady=15, padx=10)

        player_box.pack(pady=10)

        if not isinstance(player, Berserker):
            options = enumerate(["Attack", "Defend" if not isinstance(player, Shaman) else "Heal", f"{player.unique_option_name}"])
            w = 360
        else:
            w = 250
            options = enumerate(["Attack", "Defend" if not isinstance(player, Shaman) else "Heal"])

        player_options = ctk.CTkFrame(land, width=w, height=80)
        for i, btn in options:
            option = ctk.CTkButton(player_options, text=btn, width=100, height=40, state="disabled",
                                   command=player.options[i] if i != 0 else lambda: player.attack(enemy, enemy_health),
                                   font=("Silkscreen", 18), fg_color="#343645", hover_color="#23242E", border_spacing=5)
            option.pack(pady=15, padx=10, side="left")
            option.bind("<Button-1>", lambda e: self.toggle_moves())
            self.player_buttons.append(option)

        player.option_buttons = CMS.player_buttons = self.player_buttons
        CMS.enemy = enemy
        CMS.player = player
        CMS.player_hpb = player_health

        player_options.pack_propagate(False)
        player_options.pack()
        self.updateable_ui()
        self.toggle_moves()

    def death_screen(self):
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()

        self.death_scr = ctk.CTkFrame(self.tabview.tabs["Fight"], fg_color="#cccccc")
        self.death_scr.pack(expand=True, fill="both")

        death_message = ctk.CTkFrame(self.death_scr)
        heading = ctk.CTkLabel(death_message, text="You Lose!", font=self.my_font)
        description = ctk.CTkLabel(death_message, text=f"You lose to {CMS.enemy}\n"
                                                       f"at {CMS.location.loc_type} location", font=self.my_font)
        button = ctk.CTkButton(death_message, text="Back to menu", command=lambda: self.fight_ui(), font=self.my_font,
                               fg_color="#343645", hover_color="#23242E", border_spacing=5)

        heading.pack(pady=10, padx=10)
        description.pack(pady=10, padx=10)
        button.pack(pady=10, padx=10)

        death_message.pack(pady=150)

        self.selected_char = None

    def tutorial_ui(self):
        land = self.tabview.tabs["Tutorial"]

        label = ctk.CTkLabel(land, text="Character Tutorial", font=("Silkscreen", 30))
        label.pack(pady=(100, 10))

        self.frame = ctk.CTkFrame(land)
        for i in ["Warrior", "Shaman", "Berserker"]:
            char = eval(f"{i}()")
            char_frame = ctk.CTkFrame(self.frame)
            name = ctk.CTkLabel(char_frame, text=i, font=("Silkscreen", 14))
            image = ctk.CTkLabel(char_frame, text="", width=50, height=50,
                                 image=ctk.CTkImage(Image.open(f"Images/{i}.png"), size=(100, 100)))
            info = ctk.CTkLabel(char_frame, text=f"{char}", font=("Silkscreen", 14))

            name.pack(pady=5)
            image.pack(pady=5)
            info.pack(pady=5, padx=5)
            char_frame.pack(side="left", pady=20, padx=15)

        self.frame.pack(pady=(20, 0))

    def give_up(self):
        if self.give_up_l.cget("text") == "You sure?":
            CMS.round_counter = 1
            CMS.location_i = 1
            CMS.turn_counter = 0
            self.fight_ui()
        self.give_up_l.configure(text="You sure?")

    def init_win(self):
        if CMS.run_info:
            CMS.run_info.place_forget()

        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()

        frame = ctk.CTkFrame(self.tabview.tabs["Fight"])

        heading = ctk.CTkLabel(frame, text="Victory!", font=("Silkscreen", 30))
        heading.pack(pady=10)

        reward = ctk.CTkLabel(frame, font=self.my_font, text="1+ Diamond")
        reward.pack(pady=10)

        button = ctk.CTkButton(frame, text="Back to menu", font=self.my_font, command=self.fight_ui,
                               fg_color="#343645", hover_color="#23242E", border_spacing=5)
        button.pack(pady=10)

        frame.pack(pady=150)

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as s_file:
            json.dump({
                "diamonds": CMS.diamonds,
                "w_upgrade": CMS.w_upgrade,
                "s_upgrade": CMS.s_upgrade,
                "b_upgrade": CMS.b_upgrade
            }, s_file, indent=4, ensure_ascii=False)
        self.destroy()

    def store_ui(self):
        main_frame = ctk.CTkFrame(self.tabview.tabs["Store"])

        label = ctk.CTkLabel(self.tabview.tabs["Store"], text="Store", font=("Silkscreen", 30))
        label.pack(pady=(80, 30))

        diamond_counter = ctk.CTkFrame(self.tabview.tabs["Store"])

        CMS.counter = ctk.CTkLabel(diamond_counter, text=f"Diamonds\n{CMS.diamonds}", font=self.my_font)
        CMS.counter.pack(pady=10, padx=10)

        diamond_counter.place(x=10, y=10)

        for name, upg, desc, upg_var in (
            ("Warrior", "Sword", "Warrior buff\nnow is 3x"),
            ("Shaman", "Potion", "Heal provides\nfull recovery"),
            ("Berserker", "Blood Drop", "More damage\nfor health loss")
        ):
            frame = ctk.CTkFrame(main_frame)
            heading = ctk.CTkLabel(frame, text=f"{name}\n{upg}", font=self.my_font)
            image = ctk.CTkLabel(frame, text="", width=75, height=75, image=ctk.CTkImage(Image.open(f"Images/{upg}.png"), size=(75, 75)))
            description = ctk.CTkLabel(frame, text=desc+"\n1 diamond", font=self.my_font)
            button = ctk.CTkButton(frame, text="Buy", command=lambda u=upg: self.buy_upg(u), font=self.my_font,
                                   fg_color="#343645", hover_color="#23242E", border_spacing=5)

            heading.pack()
            image.pack()
            description.pack(padx=10, pady=10)
            button.pack()
            frame.pack(side="left", padx=20, pady=20)
        main_frame.pack()

    def buy_upg(self, upgrade):
        if CMS.diamonds:
            if upgrade == "Sword":
                CMS.w_upgrade = True
            elif upgrade == "Potion":
                CMS.s_upgrade = True
            else:
                CMS.b_upgrade = True
            CMS.diamonds -= 1
            CMS.counter.configure(text=f"Diamonds\n{CMS.diamonds}")

    @staticmethod
    def load_data():
        def insert_data(data):
            CMS.diamonds = data["diamonds"]
            CMS.w_upgrade = data["w_upgrade"]
            CMS.s_upgrade = data["s_upgrade"]
            CMS.b_upgrade = data["b_upgrade"]
            CMS.refresh_diamond_counter()
        try:
            with open("data.json", "r", encoding="utf-8") as l_file:
                insert_data(json.load(l_file))
        except FileNotFoundError:
            insert_data({
                "diamonds": 0,
                "w_upgrade": False,
                "s_upgrade": False,
                "b_upgrade": False
             })


class VerticalTabView(ctk.CTkFrame):
    def __init__(self, master, tabs):
        super().__init__(master)

        self.tabs = {}
        self.buttons = []
        self.current_tab = None
        self.current_button = None
        self.my_font = ctk.CTkFont(family="Silkscreen", size=18)

        self.left_frame = ctk.CTkFrame(self, width=200, fg_color="#3EA83E", corner_radius=0)
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.logo = ctk.CTkLabel(self.left_frame, text="", width=150, height=150, image=ctk.CTkImage(Image.open("Images/Logo.png"), size=(150,150)))
        self.logo.pack(pady=(40, 20))
        for name in tabs:
            btn = ctk.CTkButton(self.left_frame, text=name, width=150, height=40, font=self.my_font)
            btn.configure(command=lambda b=btn, n=name: self.switch_tab(n, b))
            btn.pack(pady=10)

            frame = ctk.CTkFrame(self.right_frame, corner_radius=0)
            self.tabs[name] = frame
            self.buttons.append(btn)
        self.switch_tab(list(tabs.keys())[0], self.buttons[0])

    def switch_tab(self, name, btn):
        if self.current_tab:
            self.tabs[self.current_tab].pack_forget()
        self.tabs[name].pack(fill="both", expand=True)
        self.current_tab = name

        for button in self.buttons:
            button.configure(fg_color="transparent", hover_color="#308E30", text_color="white")
        btn.configure(fg_color="white", hover_color="gray92", text_color="black")
        self.current_button = btn
