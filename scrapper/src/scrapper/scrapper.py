import argparse
import re

from ai_text_simplifier import simplify_paragraphs

from wiki_scrapper import URLNotValidException, scrap_wiki

BASE_QUESTION = "Simplify, make very short bullet points out of this text and give it a title:"


def check_url_validity(url: str):
    pattern = re.compile("^https:\/\/[a-z]{2}.wikipedia.org\/wiki\/[\w]*")
    match = pattern.findall(url)
    if not match or match[0] != url:
        raise URLNotValidException("Only Wikipedia URLs are supported.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scrapes wikipedia article and simplifies it with OpenAI API.')
    parser.add_argument('url', metavar='url', type=str,
                        help='URL of the wikipedia article to be scraped.')
    parser.add_argument('--o', metavar='output', type=str,
                        help='Path to the output file.')
    parser.add_argument('--q', metavar='query', type=str,
                        help='A question to be asked about the article.')

    args = parser.parse_args()

    check_url_validity(args.url)

    wiki_text = scrap_wiki(args.url)

    question = args.q if args.q else BASE_QUESTION

    simplified = simplify_paragraphs(wiki_text, question)

    with open(args.o if args.o else "output.txt", "w") as file:
        file.write("\n".join(simplified))
