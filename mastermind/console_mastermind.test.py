from ConsoleMastermind import Mastermind
import random
from typing import List

class RandomTest(Mastermind):
    won: bool = False

    def __init__(self, inputs = None, random_row: List[List] = [], **kwargs):
        super().__init__(**kwargs)
        self.inputs = inputs
        self.random_row: List[List] = random_row

    def get_random_numbers(self) -> List[int]:
        if self.multiple_appearance:
            random_numbers = []
            [random_numbers.append(random.randint(1, 8)) for i in range(0, self.max_numbers)]
        else:
            random_numbers = random.sample(range(1, 8), self.max_numbers)
        self.random_row = random_numbers
        return random_numbers

    def get_user_numbers(self):
        user_numbers = []
        [user_numbers.append(random.randint(1, 8)) for i in range(0, self.max_numbers)]
        if self.inputs is None:
            self.inputs = []
        self.inputs.append(user_numbers)
        return user_numbers

    def check_game_state(self, right, random_numbers):
        f = open("test_log.txt", "a")
        if right == 4:
            print("GEWONNEN | VERSUCHE: {} | ZUFFALSZAHLEN: {} | INPUTS: {}\n".format(self.tries, self.random_row, self.inputs))
            f.write("GEWONNEN | VERSUCHE: {} | ZUFFALSZAHLEN: {} | INPUTS: {}\n".format(self.tries, self.random_row, self.inputs))
            self.won = True
        else:
            self.tries += 1
            if self.tries >= self.max_tries+1:
                print("VERLOREN | ZUFFALSZAHLEN: {} | INPUTS: {}\n".format(self.random_row, self.inputs))
                f.write("VERLOREN | ZUFFALSZAHLEN: {} | INPUTS: {}\n".format(self.random_row, self.inputs))
            else:
                f.close()
                self.compare_rows(random_numbers)
        f.close()

class Test():
    tests = 1
    won = 0

    def __init__(self, test_anzahl: int):
        self.test_anzahl: int = test_anzahl

    def random_test(self):
        f = open("test_log.txt", "w")
        f.write("")
        f.close()
        for x in range(self.test_anzahl):
            f = open("test_log.txt", "a")
            f.write("TEST: {} | ".format(self.tests))
            f.close()
            print("TEST: {}".format(self.tests))
            Probe = RandomTest(testing=True)
            Probe.run()
            if Probe.won:
                self.won += 1
            del Probe
            self.tests += 1
        print("GEWINNE: {} | VERLUSTE: {}".format(self.won, self.test_anzahl-self.won))
        f = open("test_log.txt", "a")
        f.write("GEWINNE: {} | VERLUSTE: {}".format(self.won, self.test_anzahl-self.won))
        f.close()
    
    # Automatisch spielen
    def auto_play():
        pass

def main():
    Tst = Test(test_anzahl=1000)
    Tst.random_test()

if __name__ == '__main__':
    main()
