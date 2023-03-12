from scrapper.wiki_scrapper import scrap_wiki
from scrapper.test.wiki_test_cases import links_to_raw_text

texts_to_test = []
for link_text_dict in links_to_raw_text:
    page = scrap_wiki(link_text_dict["link"])

    raw_paragraph = page[0]
    raw_paragraph = raw_paragraph.replace("\n", "")
    raw_paragraph = raw_paragraph.replace(" ", "")
    raw_paragraph = raw_paragraph.lower()

    raw_correct_paragraph = link_text_dict["text"]
    raw_correct_paragraph = raw_correct_paragraph.replace("\n", "")
    raw_correct_paragraph = raw_correct_paragraph.replace(" ", "")
    raw_correct_paragraph = raw_correct_paragraph.lower()

    texts_to_test.append({
        "raw_first_paragraphs": (raw_paragraph, raw_paragraph),
        "number_of_paragraphs": (link_text_dict["number_of_paragraphs"], len(page))
    })


def test_integrity():
    for test_object in texts_to_test:
        assert test_object["raw_first_paragraphs"][0] == test_object["raw_first_paragraphs"][1]


def test_number_of_paragraphs():
    for index, test_object in enumerate(texts_to_test):
        assert test_object["number_of_paragraphs"][0] == test_object["number_of_paragraphs"][
            1], f"In link {links_to_raw_text[index]['link']}"
