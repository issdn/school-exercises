import requests as reqs
from bs4 import BeautifulSoup as bs
from pprint import pprint


def get_queries(url):
    req = reqs.get(url)
    assert req.status_code != 404, f"❌ 404. {url} is an incorrect url."
    soup = bs(req.content, "html.parser")
    return soup.find_all("a", class_="Link--primary")


def get_subdir_urls(user, repository, branch, ext):
    """
    Return exaple:
    relative directory path (tree)  : all files (blobs) in directory.
    {'server/server-files/routes': ['books.ts', 'users.ts']}
    """
    dirs = {}

    def get_subdir_url(
        url=f"/{user}/{repository}/file-list/{branch}",
    ):
        queries = get_queries("https://github.com" + url)
        for query in queries:
            href = query["href"].split("/")
            # path to repo files/dirs always starts after branch name
            #   -> issdn/Bibliothek/tree/master | /api
            if branch in href:
                branch_index = href.index(branch)
                if href[branch_index - 1] == "tree":
                    # href -> /user/repository/files
                    # href -> /user/repository/tree/subdirectory/file
                    # href -> /user/repository/blob/file
                    get_subdir_url(query["href"])
                    print(query["href"])
                elif href[branch_index - 1] == "blob":
                    try:
                        # Check extension like: file.py -> py
                        if query.attrs["title"].split(".")[-1:][0] in ext:
                            rel_path = "/".join(href[branch_index + 1 : -1])
                            curfile = href[-1:][0]
                            if rel_path in dirs:
                                dirs[rel_path].append(curfile)
                            else:
                                dirs[rel_path] = [curfile]
                            print("    - ", curfile)
                    except (AttributeError, KeyError):
                        pass

    print("\n⌛ Scraping all files from ", repository)
    get_subdir_url()
    print("✅ Scraped all files from ", repository)
    return dirs


if __name__ == "__main__":
    dirfiles = get_subdir_urls(
        user="issdn",
        repository="Bibliothek",
        branch="master",
        ext=["java", "js", "ts", "py", "ps1", "html", "css", "tsx", "jsx"],
    )

    pprint(dirfiles)
