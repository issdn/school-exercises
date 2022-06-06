from tokenize import Triple
from minirpg.characters import Player, Enemy
from minirpg.gui import DecisionMenu


class RPG:
    def __init__(self):
        ...

    def save(self):
        pass

    def safe_exit(self):
        pass

    def validate(self):
        pass

    def prepare_location(self):
        pass

    def player_teleport(self):
        pass


class Combat:
    def __init__(self, player: Player, enemy: Enemy) -> None:
        self._player: Player = player
        self._enemy: Enemy = enemy
        self._end: bool = False

    def print_info(self) -> None:
        print(f"{self._player.name} vs {self._enemy.name}")

    def player_attack(self) -> None:
        if self._end:
            return
        self._player.show_hp()
        self._enemy.show_hp()
        dm = DecisionMenu(
            {
                "Attack": lambda: self._enemy.take_dmg(self._player.attack()),
                "Heal": self._player.heal,
                "Flee": lambda: self._player.flee(self.end),
            }
        )
        dm.build()
        self._validate(True)

    def enemy_attack(self) -> None:
        if self._end:
            return
        self._player.take_dmg(self._enemy.attack())
        self._validate(False)

    def _validate(self, player_last_attack: bool) -> None:
        if player_last_attack:
            if not self._enemy.check_hp():
                print("You won!")
                self.end()
            self.enemy_attack()
        elif not self._player.check_hp():
            print("You're dead")
            self.end()
        self.player_attack()

    def end(self, result: str = None):
        self._end = True
        self._player.show_hp()
        self._enemy.show_hp()
