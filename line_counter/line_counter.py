import os
from os.path import isfile, isdir, join

md_path = f"{os.environ['ReadmeDir']}\README.md"
path = "..\\"
ignore = [".git", "env", "__pycache__", ".vscode"]
allowed_extensions = ["py", "js", "ts", "tsx", "ps1"]

files = []


def tree(path=path):
    for item in os.listdir(path):
        pth = join(path, item)
        if isdir(pth) and item not in ignore:
            tree(pth)
        elif isfile(pth) and item.split(".")[1:][0] in allowed_extensions:
            files.append(pth)


tree()

lines = sum(
    1 for file in files for line in open(file, encoding="utf-8").read() if len(line)
)

readme = f"""
👋 Hi, I'm Karol!\n
👉 I have currently written **{lines}** lines in my **\\school-exercises** repository!\n
📄 This was generated automatically and the code you can find in school-exercises.
"""

with open(md_path, "w+", encoding="utf-8") as md:
    md.write(readme)
    print("----README UPDATED----\n", md.read())
