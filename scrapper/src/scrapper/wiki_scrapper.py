import pprint
import requests
from bs4 import BeautifulSoup as bs, ResultSet


class URLNotValidException(Exception):
    pass


def clear(soup, tag, attrs={}):
    """Removes all elements with the given tag and attributes from the soup."""
    elements_to_clear = soup.find_all(tag, attrs)
    for element in elements_to_clear:
        element.decompose()

    return soup


def get_text(soup):
    """Returns the text of the soup."""
    if isinstance(soup, ResultSet):
        text = ""
        for element in soup:
            text += element.text
        return text
    return soup.text


def scrap_wiki(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise URLNotValidException("Page with that URL does not exist.")
    soup = bs(r.text, "lxml")

    soup = soup.find("div", {"id": "mw-content-text"})
    soup = clear(soup, "sup", {"class": "reference"})
    soup = clear(soup, "a", {"class": "autonumber"})
    soup = clear(soup, "span", {"class": "mw-editsection"})
    soup = clear(soup, "table")
    soup = clear(soup, "p", {"class": "mw-empty-elt"})
    return [tag.text for tag in soup.find_all("p")]


def get_wiki_first_paragraph(url) -> str:
    # Returns the first paragraph of the first section of the page.
    return scrap_wiki(url)[0]


def get_wiki_paragrarphs_to_text(url) -> str:
    # Returns text from the whole page.
    paragraphs = scrap_wiki(url)
    text = " ".join(paragraphs)
    return text


if __name__ == "__main__":
    page = scrap_wiki(
        "https://en.wikipedia.org/wiki/2023_Estonian_parliamentary_election")
    pprint.pprint(page)
    print("Number of paragraphs:", len(page))
