import requests as reqs
from bs4 import BeautifulSoup as bs
import re
from scraper import get_subdir_urls
from pprint import pprint
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")


class GithubScraper:
    def __init__(self, user: str, extensions: list[str]) -> None:
        self.user: str = user
        self.ext: list[str] = extensions

    def clear_dict(self, files) -> None:
        """
        {
            'Bibliothek': {
                'files': {
                    'java': 0,
                    'js': 5,
                    'ts': 0,
                    'py': 34,
                    'ps1': 1,
                    'html': 2,
                    'css': 1,
                    'tsx': 0,
                }
            ...
            }
        ...
        }

        IS CLEARED TO

        {
        'Bibliothek': {
            'files': {
                'css': 1,
                'html': 2,
                'js': 5,
                'ps1': 1,
                'py': 34
                }
            ...
            }
        ...
        }

        """
        to_remove = {}
        for repo, data in files.items():
            for data_type, data_by_extension in data.items():
                for extension, number in data_by_extension.items():
                    if number == 0:
                        if repo in to_remove:
                            if data_type in to_remove[repo]:
                                to_remove[repo][data_type].append(extension)
                            else:
                                to_remove[repo][data_type] = [extension]
                        else:
                            to_remove[repo] = {data_type: [extension]}
        for r, to_remove_data_types in to_remove.items():
            for data_type, extension_list in to_remove_data_types.items():
                for item in extension_list:
                    del files[r][data_type][item]
        return files

    # These should probably be overloaded.
    def save_to_csv(self, path, files):
        with open(path, "w") as f:
            for kr, vr in files.items():
                f.write(kr)
                for k, v in vr.items():
                    f.write(f"\n{k}={v}")
            print("Saved to: ", path)

    def save_to_csv_with_extensions(self, path, files):
        """
        WARNING
        IT ADDS ONE EMPTY LINE AT THE END

        Similar algorithm to clear_dict().

        EXAMPLE

        {'Bibliothek':
            {'files': {'html': 1, 'py': 1, 'ts': 15, 'tsx': 26},
            'letters': {'html': 48, 'py': 1267, 'ts': 13157, 'tsx': 22357},
            'lines': {'html': 4, 'py': 43, 'ts': 659, 'tsx': 1083}
        },

        WILL BE SAVED TO

        Bibliothek
        files:ts=15,py=1,html=1,tsx=26
        lines:ts=659,py=43,html=4,tsx=1083
        letters:ts=13157,py=1267,html=48,tsx=22357
        tiny-projects
        ...
        """
        with open(path, "w") as f:
            for repo, data_types in files.items():
                f.write(repo + "\n")
                for data_type, data in data_types.items():
                    index = 1
                    lenext = len(data)
                    f.write(data_type + ":")
                    for extension, number in data.items():
                        if index == lenext:
                            f.write(f"{extension}={number}\n")
                        else:
                            f.write(f"{extension}={number},")
                        index += 1

            print("Saved to: ", path)

    def count(self, user, repository, branch, files):
        numbers = {
            "nr_subdirectories": len(files.keys()),
            "nr_files": 0,
            "nr_lines": 0,
            "nr_letters": 0,
        }
        print("\n🌈 Counting in ", repository)
        for dir, files_ in files.items():
            for file in files_:
                nr_files += 1
                url = f"https://raw.githubusercontent.com/{user}/{repository}/{branch}/{dir}/{file}"
                req = reqs.get(url)
                soup = bs(req.content, "html.parser")
                parsed = re.split("\n+", soup.get_text().replace(" ", ""))
                for line in parsed:
                    nr_letters += len(line)
                    nr_lines += 1
                print(f"✅ File {file} done.")
        return numbers

    def count_w_extensions(self, user, repository, branch, files):
        numbers = {"files": {}, "lines": {}, "letters": {}}
        for v in numbers.values():
            for e in self.ext:
                v[e] = 0
        # nr_subdirectories = len(files.keys())
        print("\n🌈 Counting in ", repository)
        for dir, files_ in files.items():
            for file in files_:
                file_ext = file.split(".")[-1:][0]
                numbers["files"][file_ext] += 1
                url = f"https://raw.githubusercontent.com/{user}/{repository}/{branch}/{dir}/{file}"
                req = reqs.get(url)
                soup = bs(req.content, "html.parser")
                parsed = re.split("\n+", soup.get_text().replace(" ", ""))
                for line in parsed:
                    numbers["letters"][file_ext] += len(line)
                    numbers["lines"][file_ext] += 1
                print(f"✅ File {file} done.")
        # numbers["all"] = {}
        # numbers["all"]["nr_subdirectories"] = nr_subdirectories
        return numbers

    def get_all(self, repositories_w_branches, extensions=False):
        repos = repositories_w_branches
        for repo, branch in repositories_w_branches.items():
            files = get_subdir_urls(self.user, repo, branch, self.ext)
            if extensions:
                repos[repo] = self.count_w_extensions(self.user, repo, branch, files)
            else:
                repos[repo] = self.count(self.user, repo, branch, files)
        repos = self.clear_dict(repos)
        print("🌴 Here are your numbers: ")
        pprint(repos)
        return repos

    def get_and_save(self, path, repositories_w_branches, extensions=False):
        if extensions:
            repos = self.get_all(repositories_w_branches, True)
            self.save_to_csv_with_extensions(path, repos)
        else:
            repos = self.get_all(repositories_w_branches, False)
            self.save_to_csv(path, repos)


if __name__ == "__main__":
    gs = GithubScraper(
        "issdn", ["java", "js", "ts", "py", "ps1", "html", "css", "tsx", "svelte"]
    )
    gs.get_and_save(
        "./counted_files.txt",
        {"Bibliothek": "master", "tiny-projects": "main", "issdn-website": "master"},
        True,
    )
