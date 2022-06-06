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
        return int(x ** 2)

    def __add__(self, other):
        return Attribute(self.__func, self.value + other)

    def __str__(self):
        return str(self.value)


class Character:
    def __init__(self, name: str) -> None:
        self.__exp: int = 0
        self.__next_lvl_exp: Attribute = Attribute("square", 50)
        self.__hp: Attribute = Attribute("linear_qrt", 10)
        self.__attack_damage = Attribute("linear", 8)
        self.level: Attribute = Attribute("increment", 50)
        self.name: str = name
        self.location = Location("Oasis", "Oasis")
        self.location.oasis()

    def __repr__(self) -> str:
        return f"Name: {self.name}\nHP: {self.__hp}\nLEVEL: {self.level}\nEXP: {self.__exp}\nEXP TO NEXT LEVEL: {self.__next_lvl_exp}"

    def stats(self):
        print("\n[STATS]")
        print("------------")
        print(f"[EXP]   {self.__exp}")
        print(f"[HP]   {self.__hp}")
        print(f"[ATK]   {self.__attack_damage}")

    def __check_state(self):
        ...

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

    def take_damage(self, damage: int):
        self.__hp -= damage


class Player(Character):
    def __init__(self, player_class: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_class: str = player_class

    def status(self):
        pass

class Location:

    type_oasis = 'Oasis'
    type_desert = 'Desert'
    type_forest = 'Forest'
    type_mountain = 'Mountain'

    def __init__(self, name, type_of):
        self.name = name
        self.type_of = type_of

    def desert(self, name):
        self.name = name
        self.type_of = self.type_desert

    def oasis(self):
        self.name = self.name
        self.type_of = self.type_oasis
        return self.type_oasis

    def forest(self, name):
        self.name = name
        self.type_of = self.type_forest

    def mountain(self, name):
        self.name = name
        self.type_of = self.type_mountain

    def start_location(self):
        self.oasis('Start location')

    def sahara_desert(self):
        self.desert('Sahara Desert')

    def maple_forest(self):
        self.forest('Maple forest')

    def mountain_forest(self):
        self.mountain('Mountain forest')

    def winter_forest(self):
        self.mountain('Winter forest')




class Debuff:
    def __init__(self, damage):
        self.damage = damage

    def set_location_damage(self):
        if Location.type_of == Location.type_oasis:
            print("You wont get any damage.")
            self.damage = 0
        if Location.type_of == Location.type_desert:
            print("You will get sand damage.")
            self.damage = 1
        if Location.type_of == Location.type_forest:
            print("You will get tree damage.")
            self.damage = 2
        if Location.type_of == Location.type_mountain:
            print("You will get rock damage.")
            self.damage = 3



    def lava_attack(self):
        print('Every round you will take damage')
        Character.take_dmg(self.damage * 2)

player = Player("Bogenschützer" ,"Nishero")
print(player.location.type_of)


