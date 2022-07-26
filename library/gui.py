from tkinter import Label


class SuperLabel(Label):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
