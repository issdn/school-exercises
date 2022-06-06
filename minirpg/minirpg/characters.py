from typing import Any, Callable, Iterable
from minirpg.config import Config
from minirpg.miscellaneous import Item, Spell
from minirpg.gui import ProgressBar
from minirpg.locations import Location
import random

class Debuff:
    def __init__(self, damage):
        self.damage = damage
        self.location = Location("name", "type")

    def set_location_damage(self):
        if self.location.type_of == self.location.type_oasis:
            print("You wont get any damage.")
            self.damage = 0
        if self.location.type_of == self.location.type_desert:
            print("You will get sand damage.")
            self.damage = 1
        if self.location.type_of == self.location.type_forest:
            print("You will get tree damage.")
            self.damage = 2
        if self.location.type_of == self.location.type_mountain:
            print("You will get rock damage.")
            self.damage = 3

    def lava_attack(self):
        print("Every round you will take damage")
        Character.take_dmg(self.damage * 2)

    def sand_storm(self):
        Character.take_dmg(self.damage)


class Attack:
    def __init__(self, name: str, type: str) -> None:
        self.name: str = name
        self.type: str = type

    @staticmethod
    def yeld_standard_dmg(base_dmg: int) -> int:
        return base_dmg


class Attribute:
    def __init__(self, func: Callable | str, value: int = 0) -> None:
        self.value: int = value
        if callable(func):
            self.__func = func
        elif type(func) is str:
            self.__func = getattr(self, func)

    def level_up(self) -> None:
        """Increases attribute with an attribute function."""
        self.value = self.__func(self.value)

    def increment(self, x: int) -> int:
        return int(x + 1)

    def linear_qrt(self, x: int) -> int:
        return int(x * 1.25)

    def linear_half(self, x: int) -> int:
        return int(x * 1.5)

    def linear(self, x: int) -> int:
        return int(x * 2)

    def square(self, x: int) -> int:
        return int(x**2)

    def __add__(self, other) -> object:
        return Attribute(self.__func, self.value + other)

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def pretty_string(name: str, value: Any) -> str:
        """Returns padded name and value."""
        return "{placeholder_name:<8}{placeholder_value}".format(
            placeholder_name=name, placeholder_value=str(value)
        )


class Character:
    """Parent class for both Player and Enemy."""

    def __init__(self, name: str) -> None:
        """
        :int _exp - current amount of exp.
        :Attribute _next_lvl_exp - exp needed for next level.
        :Attribute _max_hp - max hp. Constant. Only level up can change it.
        :int _hp - current hp. Mutable during combat, healing etc.
        :Attribute _attack_damage - Basic attack damage of character. Mutable with for eg. Items.
        :ProgressBar _hppb - Prettier HP visualisation. Relative to :_hp and :_max_hp.
        :Attribute _attacks - Mutable dictionary of character's attacks.
        :Attribute level - Can be only incremented. Increments by 1 when exp reaches next_lvl_exp.
        :str name - Name of the character.
        """

        self._exp: int = 0
        self._next_lvl_exp: Attribute = Attribute("square", 50)
        self._max_hp: Attribute = Attribute("linear_qrt", 10)
        self._hp: int = self._max_hp.value
        self._attack_damage = Attribute("linear", 8)
        self._hppb: ProgressBar = ProgressBar(self._max_hp.value, self._hp)
        self._attacks: Iterable[Attack] = []
        self.level: Attribute = Attribute("increment", 0)
        self.name: str = name

    def __repr__(self) -> str:
        return f"{id(self)} CHARACTER"

    def show_hp(self) -> None:
        print(Attribute.pretty_string(f"{self.name} HP", self._hppb.get()))

    def status(self) -> str:
        print(f"\n{self.name.upper()}")
        print(Config.spacer)
        print(Attribute.pretty_string("HP", self._hppb.get()))

    def take_dmg(self, amount: int) -> None:
        """
        Calculates the damage to be taken from HP,
        substracts it and updates the HP Bar.
        """

        self._hp -= amount
        self.check_hp()
        self._hppb.update(current=self._hp)

    def flee(self, callback: Callable) -> None:
        percentage = random.randint(1, 101)
        if percentage in range(1, 61):
            print("You successfully ran away!")
            callback()
        else:
            print("Fled unsuccessfully!")

    def attack(self, attack: Attack = None) -> int:
        """Returns damage to be dealt."""

        return Attack.yeld_standard_dmg(self._attack_damage.value)

    def heal(self, item: Item = None, spell: Spell = None) -> None:
        """Heals the character with spell or item."""
        self._hp += 10
        # if item is not None:
        #     item.use(self)
        #     return
        # if spell is not None:
        #     spell.use(self)

    def add_exp(self, amount: int) -> None:
        """Adds exp to character."""

        self._exp += int(amount)
        self._check_exp()

    def _check_exp(self) -> None:
        """Checks if :self._exp is higher than :self._next_level_exp
        and if it so, calls the self._level_up function."""

        if self._exp == self._next_lvl_exp:
            self._level_up()
        elif self._exp > self._next_lvl_exp:
            additional_exp = self._exp - self._next_lvl_exp
            self._level_up()
            self._exp += additional_exp
            self._check_state()

    def check_hp(self) -> bool:
        """Cheks whether the hp is or is below 0."""

        if self._hp <= 0:
            return False
        return True


class Player(Character):
    def __init__(self, player_class: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_class: str = player_class
        self._exppb: ProgressBar = ProgressBar(self._next_lvl_exp.value, self._exp)
        # self.location: Location = Location.oasis

    def info(self) -> None:
        """Prints main info."""

        print(f"\n{self.name.upper()}")
        print(Config.spacer)
        print(Attribute.pretty_string("LVL", self.level))
        print(Attribute.pretty_string("EXP", self._exppb.get()))

    def status(self) -> None:
        """Prints all character's attributes."""

        print(f"\n{self.name.upper()} STATS")
        print(Config.spacer)
        print(Attribute.pretty_string("LVL", self.level))
        print(Attribute.pretty_string("EXP", self._exppb.get()))
        print(Attribute.pretty_string("HP", self._hppb.get()))
        print(Attribute.pretty_string("ATK", self._attack_damage))

    def __level_up(self) -> None:
        """Calls level_up on every character's attribute."""

        print("--- LEVEL UP ---")
        self._next_lvl_exp.level_up()
        self._hp.level_up()
        self._attack_damage.level_up()
        self.level.level_up()


class Enemy(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
