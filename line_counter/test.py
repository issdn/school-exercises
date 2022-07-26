from github_counter import *
from pprint import pprint

repos_example = {
    "Bibliothek": {
        "files": {
            "java": 0,
            "js": 5,
            "ts": 0,
            "py": 34,
            "ps1": 1,
            "html": 2,
            "css": 1,
            "tsx": 0,
        },
        "lines": {
            "java": 0,
            "js": 457,
            "ts": 0,
            "py": 2290,
            "ps1": 10,
            "html": 9,
            "css": 175,
            "tsx": 0,
        },
        "letters": {
            "java": 0,
            "js": 11274,
            "ts": 0,
            "py": 55523,
            "ps1": 233,
            "html": 48,
            "css": 3004,
            "tsx": 0,
        },
    },
    "tiny-projects": {
        "files": {
            "java": 0,
            "js": 5,
            "ts": 0,
            "py": 34,
            "ps1": 1,
            "html": 2,
            "css": 1,
            "tsx": 0,
        },
        "lines": {
            "java": 0,
            "js": 457,
            "ts": 0,
            "py": 2290,
            "ps1": 10,
            "html": 9,
            "css": 175,
            "tsx": 0,
        },
        "letters": {
            "java": 0,
            "js": 11274,
            "ts": 0,
            "py": 55523,
            "ps1": 233,
            "html": 48,
            "css": 3004,
            "tsx": 0,
        },
    },
}

if __name__ == "__main__":
    gs = GithubScraper("issdn", ["java", "js", "ts", "py", "ps1", "html", "css", "tsx"])
    clean_repos = gs.clear_dict(repos_example)
    pprint(clean_repos)
    # gs.save_to_csv_with_extensions("./counted_files.txt", clean_repos)
    # files = get_subdir_urls(
    #     "issdn",
    #     "tiny-projects",
    #     "main",
    #     ["java", "js", "ts", "py", "ps1", "html", "css", "tsx"],
    # )
    # repos = gs.count_w_extensions("issdn", "tiny-projects", "main", files)
    # pprint(repos)
