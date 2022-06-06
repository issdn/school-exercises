from typing import Callable


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
        """Linear function returning value of x+1"""
        return int(x + 1)

    def linear_qrt(self, x: int) -> int:
        """Linear function returning value of x with m = 1.25"""
        return int(x * 1.25)

    def linear_half(self, x: int) -> int:
        """Linear function returning value of x with m = 1.5"""
        return int(x * 1.5)

    def linear(self, x: int) -> int:
        """Linear function returning value of x with m = 2"""
        return int(x * 2)

    def square(self, x: int) -> int:
        """Exponential function returning value of x"""
        return int(x**2)

    def __add__(self, other):
        return Attribute(self.__func, self.value + other)

    def __str__(self):
        return str(self.value)


class Character:
    def __init__(self, name: str) -> None:
        self.__exp: int = 0
        self.__next_lvl_exp: int = Attribute("square", 50)
        self.__hp: int = Attribute("linear_qrt", 10)
        self.__attack_damage = Attribute("linear", 8)
        self.level: int = Attribute("increment", 50)
        self.name: str = name

    def __repr__(self) -> str:
        return f"[{id(self)} CHARACTER]"

    def status(self) -> str:
        print(f"\n[{self.__class__.__name__()}]")
        print("------------")
        print(f"[HP]   {self.__hp}")

    def __check_state(self):
        if self.__exp == self.__next_lvl_exp:
            self.__level_up()
        elif self.__exp > self.__next_lvl_exp:
            additional_exp = self.__exp - self.__next_lvl_exp
            self.__level_up()
            self.__exp += additional_exp
            self.__check_state()

    def __level_up(self):
        print("--- LEVEL UP ---")
        self.__next_lvl_exp.level_up()
        self.__hp.level_up()
        self.__attack_damage.level_up()
        self.level.level_up()

    def flee(self):
        ...

    def attack(self):
        ...

    def heal(self):
        ...

    def add_exp(self, amount: int):
        self.__exp += int(amount)


class Player(Character):
    def __init__(self, player_class: str, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.player_class: str = player_class

    def status(self) -> str:
        print("\n[STATS]")
        print("------------")
        print(f"[EXP]   {self.__exp}")
        print(f"[NLEXP]   {self.__next_lvl_exp}")
        print(f"[HP]   {self.__hp}")
        print(f"[ATK]   {self.__attack_damage}")


class Enemy(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
