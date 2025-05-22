import customtkinter as ctk
from models.location import *
from PIL import Image
from models.items import *


class App(ctk.CTk, CMS):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.title("Game")
        # self.iconbitmap("")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        self.selected_char = None

        self.my_font = ctk.CTkFont(family="Silkscreen", size=18)
        self.tabview = None
        self.death_scr = None
        self.start_button = None
        self.player_buttons = []

        self.create_ui()

    def create_ui(self):
        # Creating main UI component
        self.tabview = VerticalTabView(self, {"Fight": None, "Store": None, "Tutorial": None})
        self.tabview.pack(expand=True, fill="both")

        self.fight_ui()

    def fight_ui(self):
        # forgetting old widgets and create point variable for objects to pack
        if CMS.money_label:
            CMS.money_label.place_forget()

        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()

        # Buttons for game and tutorial
        self.heading = ctk.CTkLabel(self.tabview.tabs["Fight"], text="Select character", font=("Silkscreen", 30))
        self.heading.pack(pady=(80, 40))

        self.characters_f = ctk.CTkFrame(self.tabview.tabs["Fight"])
        for i, char in enumerate(["Warrior", "Shaman", "Char 3"]):
            frame = ctk.CTkFrame(self.characters_f)
            heading = ctk.CTkLabel(frame, text=f"{char}", font=self.my_font)
            img_box = ctk.CTkLabel(frame, text="", fg_color="gray", width=100, height=100)
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
            CMS.money_label = ctk.CTkLabel(self.tabview.tabs["Fight"], text=f"Money: {None}", font=self.my_font)
            CMS.money_label.place(x=10, y=10)
            self.init_fight(self.selected_char, location.enemy_encounter())

        else:
            self.heading.configure(text="You cant start a run\nif you not picked any character")

    def init_shop(self):
        self.updateable_ui()
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()
        land = self.tabview.tabs["Fight"]

        heading = ctk.CTkLabel(land, text="Shop", font=self.my_font)
        heading.pack()

        items_frame = ctk.CTkFrame(land)
        items_frame.pack()
        for item in [Item() for i in range(3)]:
            frame = ctk.CTkFrame(items_frame)
            image = ctk.CTkLabel(frame, text="", width=75, height=75, fg_color="gray")
            label = ctk.CTkLabel(frame, text=f"{item}", font=self.my_font)
            button = ctk.CTkButton(frame, text="Buy", command=lambda i=item: i.effect(), font=self.my_font)

            frame.pack(side="left")
            image.pack()
            label.pack()
            button.pack()

        button = ctk.CTkButton(land, text="Leave", command=lambda: self.toggle_moves(), font=self.my_font)
        button.pack()

    @staticmethod
    def updateable_ui():
        CMS.money_label.configure(text=f"Money: {CMS.player.money}")
        CMS.money_label.place(x=10, y=10)

    @staticmethod
    def new_location(l_type):
        new_location = Location(l_type)
        CMS.location = new_location

    def init_fight(self, player, enemy):

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

        enemy_health = ctk.CTkProgressBar(enemy_box, width=enemy.health * 2, mode="determinate", progress_color="#8C0002")
        enemy_health.set(1)
        CMS.enemy_hpb = enemy_health
        enemy_health.pack(pady=15)
        enemy_box.pack(pady=(40, 10))

        # Info between enemy and player
        info_l = ctk.CTkLabel(land, height=100, text="", font=self.my_font)
        info_l.pack()

        CMS.info_label = info_l

        # Player UI
        player_sprite = ctk.CTkLabel(land, width=125, height=125, fg_color="gray", text="")
        player_sprite.pack()

        player_health = ctk.CTkProgressBar(land, width=player.max_health * 2, mode="determinate")
        player_health.set((player.health * player.max_health / 100) / 100)
        player_health.pack(pady=15)

        player_options = ctk.CTkFrame(land, width=360, height=80)
        for i, btn in enumerate(["Attack", "Defend" if not isinstance(player, Shaman) else "Heal", f"{player.unique_option_name}"]):
            option = ctk.CTkButton(player_options, text=btn, width=100, height=40, state="disabled",
                                   command=player.options[i] if i != 0 else lambda: player.attack(enemy, enemy_health),
                                   font=("Silkscreen", 18))
            option.pack(pady=15, padx=10 , side="left")
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
                                                       f"at location number {CMS.location_i}", font=self.my_font)
        button = ctk.CTkButton(death_message, text="Back to menu", command=lambda: self.fight_ui(), font=self.my_font)

        heading.pack()
        description.pack()
        button.pack()

        death_message.pack()

        self.selected_char = None


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

        self.logo = ctk.CTkLabel(self.left_frame, text="", width=150, height=150, fg_color="gray")
        self.logo.pack(pady=(40, 20))
        for name in tabs:
            btn = ctk.CTkButton(self.left_frame, text=name, width=150, height=40, font=self.my_font)
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
            button.configure(fg_color="transparent", hover_color="#308E30", text_color="white")
        btn.configure(fg_color="white", hover_color="gray92", text_color="black")
        self.current_button = btn
