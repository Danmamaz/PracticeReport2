class Item:
    def __init__(self, player, cost, func):
        self.player = player
        self.cost = cost
        self.func = func

    def heal(self):
        self.player.health = self.player.max_health / 3


    def buy_item(self):
        self.player.money -= self.cost
        self.cost += self.cost * 1.5
        eval(f"{self.func}()")

if __name__ == '__main__':
    item = 