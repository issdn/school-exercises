from typing import Callable
from minirpg.config import Config
import utils as ut


class ProgressBar:
    def __init__(self, max: int, current: int = 0) -> None:
        self._max: int = max
        self._current: int | float = current

    def _calc(self) -> int:
        return self._current / self._max * 100

    def update(self, current: int = None, max: int = None):
        if current is not None:
            self._current = current
        if max is not None:
            self._max = max

    def get(self) -> str:
        current_bar = "▮" * int(self._calc() / 5)
        return f"[{current_bar.ljust(20, '▯')}] {self._current} / {self._max}"


class DecisionMenu:
    def __init__(self, decisions: dict[str, Callable]) -> None:
        self._decisions: dict[str, Callable] = decisions

    def _control_input(self) -> None:
        player_input = input(Config.input_prefix)
        try:
            if ut.is_int(player_input):
                list(self._decisions.values())[int(player_input) - 1]()
            else:
                return self._decisions[player_input.lower()]()
        except (KeyError, IndexError):
            self._control_input()

    def build(self) -> None:
        for number, decision in enumerate(self._decisions.keys()):
            print("%s. %s" % (number + 1, decision.capitalize()))
        self._control_input()
