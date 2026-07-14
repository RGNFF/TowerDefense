print("欢迎来玩!")
player_hp=100
gold=200
wave=1
print(f"玩家血量：{player_hp}，金幣：{gold}，波數：{wave}")
damage=30
player_hp-=damage
print(f"受到{damage}點傷害，剩餘血量：{player_hp}")