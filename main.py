import requests
from pathlib import Path
from bs4 import BeautifulSoup
from tululu import download_txt


Path("books").mkdir(parents=True, exist_ok=True)


def check_for_redirect():
    for number_books in range(1, 11):
        url = f'https://tululu.org/b{number_books}/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('h1')
        title_text = title_tag.text.split(':')
        title_text_strip = title_text[0].strip()
        filename = download_txt(url, title_text_strip)

        try:
            if response.history == []:
                with open(filename, 'wb') as file:
                    file.write(response.content)
        except requests.exceptions.HTTPError():
            raise Exception(response.url).with_traceback()

    return response


check_for_redirect()