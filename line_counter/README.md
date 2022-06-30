# Line Counter

### File Explanation

---

#### `edit_and_commit.ps1`

    1. $currLocation = Get-Location
    2. python .\line_counter.py
    3. Set-Location $Env:ReadmeDir
    4.  git add .
        $randCommitMess = Get-Random
        git commit -m "$randCommitMess"
        git push origin master
    5. Set-Location $currLocation

1. Saves your current directory.
2. Calls python script from within the same directory.
3. Sets directory to one with the README.md file you want to commit.
   This you have to either add as an environemtal variable or directly in code like: `Set-Location "./path/to/dir"`
4. 1. calls git add.
   2. yields random commit message.
   3. pushes to origin. In this case master. (For different origin just change the master.)
5. Goes back to your first, saved location.

---

#### `line_counter.py`

    1. md_path = f"{os.getenv('ReadmeDir')}\README.md"
    2. path = "..\\"
    3. ignore = [".git", "env", "__pycache__", ".vscode"]
    4. allowed_extensions = ["py", "js", "ts", "tsx", "ps1"]

    5. projects = [...]
    6. file_tree() ...
    7. size = (...)
    8. lines = (...)
    9 letters = (...)
    10. readme = ""...
    11. with open(md_path, "w", encoding="utf-8") as md:
        md.write(readme)

1. Variable for path of your README.md file.
2. Directory of your folder/files you want to count.
3. List of folder names to ignore.
4. List of extensions to allow. (at the time of writing this I realized how stupidly redundant it is lol)
5. Creates a list of folders (here every one is counted as a project) in the specified directory.
6. Creates a list of files in the specified directory.
7. Calculates the size of all the files.
8. Calculates the lines in all the files ommiting empty ones.
9. Calculates all the letters in all the files ommting empty ones and line breaks (\n).
10. Striing with with complete README.md.
11. Opens README.md from specified path in `md_path`, writes the string and closes.

---

Feel free to use if you find it useful. 🙆‍
