class GameManager:

    def __init__(self):
        self.gold = 200
        self.life = 20
        self.score = 0
        self.towers = []
def build_tower(self, tower):

    if self.gold >= tower["cost"]:

        self.gold -= tower["cost"]

        self.towers.append(tower)

        print(f"建造成功，目前金币 {self.gold}")

    else:

        print("金币不足")
def enemy_killed(self, enemy):

    self.gold += enemy["reward"]

    self.score += enemy["reward"]

    print(f"{enemy['name']} 被消灭")
def enemy_reached_base(self):

    self.life -= 1

    print(f"基地剩余生命 {self.life}")