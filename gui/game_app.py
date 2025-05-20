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

        self.tabview = None
        self.money = None
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
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()

        # Buttons for game and tutorial
        self.heading = ctk.CTkLabel(self.tabview.tabs["Fight"], text="Select character")
        self.heading.pack()

        self.characters_f = ctk.CTkFrame(self.tabview.tabs["Fight"])
        for i, char in enumerate(["Warrior", "Shaman", "Char 3"]):
            frame = ctk.CTkFrame(self.characters_f)
            heading = ctk.CTkLabel(frame, text=f"{char}")
            img_box = ctk.CTkLabel(frame, text="", fg_color="gray", width=100, height=100)
            button = ctk.CTkButton(frame, text=f"Pick", command=lambda c=char: self.select_character(c))
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
            self.money = ctk.CTkLabel(self.tabview.tabs["Fight"], text=f"Money: {None}")
            self.money.place(x=10, y=10)
            self.init_fight(self.selected_char, location.enemy_encounter())

        else:
            self.heading.configure(text="You cant start a run\nif you not picked character")

    def init_shop(self):
        self.updateable_ui()
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()
        land = self.tabview.tabs["Fight"]

        heading = ctk.CTkLabel(land, text="Shop")
        heading.pack()

        items_frame = ctk.CTkFrame(land)
        items_frame.pack()
        for item in [Item() for i in range(3)]:
            frame = ctk.CTkFrame(items_frame)
            image = ctk.CTkLabel(frame, text="", width=75, height=75, fg_color="gray")
            label = ctk.CTkLabel(frame, text=f"{item}")
            button = ctk.CTkButton(frame, text="Buy", command=lambda i=item: i.effect())

            frame.pack(side="left")
            image.pack()
            label.pack()
            button.pack()

        button = ctk.CTkButton(land, text="Leave", command=lambda: self.toggle_moves())
        button.pack()

    def updateable_ui(self):
        self.money.configure(text=f"Money: {CMS.player.money}")
        self.money.place(x=10, y=10)

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
        enemy_name_l = ctk.CTkLabel(land, text=f"{enemy.image}")
        enemy_name_l.pack(padx=10)

        enemy_sprite = ctk.CTkLabel(land, width=75, height=75, fg_color="transparent",
                                    text="", image=ctk.CTkImage(Image.open(CMS.image_enemy), size=(75, 75)))
        enemy_sprite.pack()

        enemy_health = ctk.CTkProgressBar(land, mode="determinate")
        enemy_health.set(1)
        CMS.enemy_hpb = enemy_health
        enemy_health.pack()

        # Info between enemy and player
        info_l = ctk.CTkLabel(land, height=150, text="")
        info_l.pack()

        CMS.info_label = info_l

        # Player UI
        player_sprite = ctk.CTkLabel(land, width=75, height=75, fg_color="gray", text="")
        player_sprite.pack()

        player_health = ctk.CTkProgressBar(land, mode="determinate")
        player_health.set((player.health * player.max_health / 100) / 100)
        player_health.pack()

        player_options = ctk.CTkFrame(land)
        for i, btn in enumerate(["Attack", "Defend" if not isinstance(player, Shaman) else "Heal", f"{player.unique_option_name}"]):
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
        self.updateable_ui()
        self.toggle_moves()

    def death_screen(self):
        # forgetting old widgets and create point variable for objects to pack
        for child in self.tabview.tabs["Fight"].winfo_children():
            child.pack_forget()

        self.death_scr = ctk.CTkFrame(self.tabview.tabs["Fight"], fg_color="#cccccc")
        self.death_scr.pack(expand=True, fill="both")

        death_message = ctk.CTkFrame(self.death_scr)
        heading = ctk.CTkLabel(death_message, text="You Lose!")
        description = ctk.CTkLabel(death_message, text=f"You lose to {CMS.enemy}\n"
                                                       f"at location number {CMS.location_i}")
        button = ctk.CTkButton(death_message, text="Back to menu", command=lambda: self.fight_ui())

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
