def create_character(name, hp, attack, defense):
    return {
        "name": name,
        "hp": hp,
        "attack": attack,
        "defense": defense
    }

def calculate_damage(attack, defense):
    return max(1, attack - defense)
def battle_round(attacker, defender):
    damage = calculate_damage(attacker["attack"], defender["defense"])
    defender["hp"] -= damage

    print(f"{attacker['name']} 攻击了 {defender['name']}，造成 {damage} 点伤害")
    print(f"{defender['name']} 剩余血量: {defender['hp']}")




