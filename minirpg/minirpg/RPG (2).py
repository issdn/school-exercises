import random

class Player:
    def __init__(self, name="", player_class="", hp=20, damage=10, battle_status=False):
        self.name = name
        self.hp = hp
        self.player_class = player_class
        self.damage = damage
        self.battle_status = battle_status

    def check_status(self, battle_status):
        if battle_status:
            print("You are in battle. Keep fighting!!!")
        return battle_status



class Enemy:
    def __init__(self, name="", hp=15, damage=5):
        self.name = name
        self.hp = hp
        self.damage = damage

class RPG:

    def start(self) -> Player:
        name = input(str("What's your nickname?: "))
        player_class = input(str("What's your class? (wizard, warrior, archer): ")).title()
        player = Player(name, player_class)
        return player

    def met_enemy(self) -> Enemy:
        enemy = Enemy("Goblin")
        Player.battle_status = True
        print(f"Oh no, you've met {enemy.name}!")
        return enemy

    def fight_menu(self, Player, Enemy):
        print(Player.name)
        print(Enemy.name)
        round = 0
        while Player.hp > 0 and Enemy.hp > 0 and Player.battle_status:
            round += 1
            print(f"\n ---ROUND {round}---")
            print(f'Your hp: {Player.hp}')
            print(f"Enemy's hp: {Enemy.hp}")
            act = input(str('What do you want to do?(write a number)\n1. Attack\n2. Drink health potion\n3. Flee(Chance 60/40)\n'))
            act = int(act)
            if act == 1:
                Enemy.hp -= Player.damage
                if Enemy.hp <= 0:
                    Enemy.hp = 0
                    continue
                print(f"The hp of the {Enemy.name}: {Enemy.hp} ")
            elif act == 2:
                print("You've drunk your health potion")
                Player.hp += 10
                if Player.hp >= 20:
                    Player.hp = 20
            elif act == 3:
                percentage = random.randint(1, 101)
                if percentage in range(1, 61):
                    print("You successfully ran away!")
                    Player.battle_status = False
                    continue
                else:
                    print("You couldn't run away")
            Player.hp -= Enemy.damage
            print(f'You got a damage from {Enemy.name}: {Enemy.damage} ')
        if Player.hp <= 0:
            print("You're dead")
        elif Enemy.hp <= 0:
                print("You won!")
                print(f"Your hp: {Player.hp}")
                Player.battle_status = False

Player = RPG.start(RPG)
Enemy = RPG.met_enemy(RPG)
RPG.fight_menu(RPG, Player, Enemy)







