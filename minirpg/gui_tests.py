from minirpg.gui import ProgressBar, DecisionMenu
from minirpg.characters import Attribute

attr = Attribute("linear", 500)
pb = ProgressBar(attr.value, 200)
print(pb.get())
attr.level_up()
pb.update(max=attr.value)
print(pb.get())


def x():
    print("Printed")


def f():
    print("Printed 2")


dm = DecisionMenu({"Option1": x, "Option2": f})
dm.build()
