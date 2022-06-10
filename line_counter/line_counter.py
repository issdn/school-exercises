import os
from os.path import isfile, isdir, join

md_path = f"{os.getenv('ReadmeDir')}\README.md"
path = "..\\"
ignore = [".git", "env", "__pycache__", ".vscode"]
allowed_extensions = ["py", "js", "ts", "tsx", "ps1"]

projects = [
    directory
    for directory in os.listdir(path)
    if isdir(join(path, directory)) and directory not in ignore
]


files = []


def file_tree(path=path):
    for item in os.listdir(path):
        pth = join(path, item)
        if isdir(pth) and item not in ignore:
            file_tree(pth)
        elif isfile(pth) and item.split(".")[1:][0] in allowed_extensions:
            files.append(pth)


file_tree()

size = sum(os.path.getsize(file) for file in files)

lines = sum(
    1
    for file in files
    for line in open(file, encoding="utf-8").readlines()
    if line != "\n"
)

letters = sum(
    1
    for file in files
    for letter in open(file, encoding="utf-8").read()
    if letter != " " and letter != "\n"
)


readme = f"""
👋 Hi, I'm **Karol**!\n
📌 I currently have **{len(projects)}** small projects in my *\\school-exercises* repository!\n
🧩 That's **{len(files)}** files, **{lines}** lines, **{letters}** letters and **{size}** bytes of code!\n
🤖 This was generated automatically by the code which you can find in *\\school-exercises\\line_counter*.
"""

with open(md_path, "w", encoding="utf-8") as md:
    md.write(readme)
    print("----README UPDATED----")
