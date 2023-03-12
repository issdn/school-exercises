from dotenv import load_dotenv
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class OpenAIError(Exception):
    pass


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    raise OpenAIError("OpenAI API key not set.")

LINK = "https://api.openai.com/v1/chat/completions"
HEADERS = {"Authorization": "Bearer " + openai_key}


def simplify_paragraphs(paragraphs, question):
    print(f"Simplifying {len(paragraphs)} paragraphs...")
    threads = []
    simplified = []
    done = 0
    with ThreadPoolExecutor(max_workers=50) as executor:
        for paragraph in paragraphs:
            threads.append(executor.submit(
                simplify_paragraph, paragraph, question))
        for thread in as_completed(threads):
            done += 1
            print("Simplified " + str(done) + "/" +
                  str(len(paragraphs)) + " paragraphs.")
            simplified.append(thread.result())
    return simplified


def simplify_paragraph(paragraph, question):
    json = {"model": "gpt-3.5-turbo", "messages": [
        {"role": "user", "content": question + "\n" + paragraph}]}
    result = requests.api.post(LINK, json=json, headers=HEADERS)
    if result.status_code != 200:
        raise OpenAIError("OpenAI API returned a non-200 status code.")
    return result.json()["choices"][0]["message"]["content"]
