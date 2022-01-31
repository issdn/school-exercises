import random
from typing import List

class Mastermind():

    tries: int = 1

    def __init__(self,
                 max_tries: int = 10,
                 max_numbers: int = 4,
                 multiple_appearance: bool = False,
                 show_position: bool = False,
                 debug: bool = False,
                 testing: bool = False,
                 ):
        self.max_tries: int = max_tries
        self.max_numbers: int = max_numbers
        self.multiple_appearance: bool = multiple_appearance
        self.show_position: bool = show_position
        self.debug: bool = debug
        self.testing: bool = testing

    def run(self):
        self.print_logo()

        random_numbers = self.get_random_numbers()
        if self.debug:
            print("\nZufallszahlen: {}".format(random_numbers))

        self.compare_rows(random_numbers)

    def get_user_numbers(self) -> List[int]:
        user_input = input("Deine Zahlen: ")
        user_numbers = list(map(int, user_input))

        if len(user_numbers) != self.max_numbers:
            print("Gib * {} * Zahlen ein!".format(self.max_numbers))
            self.get_user_numbers()
        else:
            return user_numbers

    def get_random_numbers(self) -> List[int]:
        if self.multiple_appearance:
            random_numbers = []
            [random_numbers.append(random.randint(1, 8)) for i in range(0, self.max_numbers)]
        else:
            random_numbers = random.sample(range(1, 8), self.max_numbers)
        return random_numbers

    def compare_rows(self, random_numbers):
        false: int = 0
        right: int = 0
        halfright: int = 0

        equals = []

        self.next_round()

        user_numbers = self.get_user_numbers()

        for i in range(len(random_numbers)):
            if user_numbers[i] == random_numbers[i]:
                equals.append(1)
                right += 1
            elif random_numbers[i] in user_numbers and user_numbers[i] != random_numbers[i]:
                halfright += 1
                for j in range(len(random_numbers)):
                    if random_numbers[i] == random_numbers[j]:
                        equals.append(2)
            else:
                equals.append(0)
                false += 1
        
        if self.show_position:
            print("\n {} \n".format(equals))

        self.helpers(false=false, right=right, halfright=halfright)

        self.check_game_state(right=right, random_numbers=random_numbers)

    def check_game_state(self, right, random_numbers):
        if right == 4:
            print("")
            print("#"*31)
            print("#"*10 + " Gewonnen! " + "#"*10)
            print("#"*31)
        else:
            self.tries += 1
            if self.tries >= self.max_tries+1:
                print("")
                print("-"*34)
                print("-- Zu viele Versuche, verloren! --")
                print("-"*34)
            else:
                self.compare_rows(random_numbers)

################################################### TEXT FUNCTIONS ####################################################

    def space_out(self, logo: str) -> str:
        final_str = '  '.join(list(logo))
        return final_str

    def print_logo(self, gleichz_anzahl: int = 32, logo: str = "MASTERMIND"):
        if not self.testing:
            print("=" * gleichz_anzahl + "\n= " + self.space_out(logo) + " =\n" + "=" * gleichz_anzahl)
            print("\nWillkommen zu Mastermind\n")

    def helpers(self, false: int , right: int, halfright: int):
        if not self.testing:
            if false != 0:
                print("{} Zahl/en ist/sind falsch! ".format(false))
            if right != 0:
                print("{} Zahl/en ist/sind richtig".format(right))
            if halfright != 0:
                print("{} Zahl/en ist/sind halbrichtig".format(halfright))

    def next_round(self):
        if not self.testing:
            print("")
            print("Versuch: {}".format(self.tries))
            print("")

def main():
    mastermind = Mastermind()
    mastermind.run()


if __name__ == '__main__':
    main()
