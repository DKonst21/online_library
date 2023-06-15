import requests
from pathlib import Path
from bs4 import BeautifulSoup
from tululu import download_txt, download_image
from urllib.parse import urljoin, unquote, urlparse


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
        comments = soup.find_all(class_='texts')
        find_genre = soup.find_all(class_='d_book')

        try:
            if response.history == []:

                download_txt(url, title_text_strip)

                image = unquote(urlparse(
                    urljoin('https://tululu.org', soup.find(class_='bookimage').find('img')['src'])).path)
                download_image(f'https://tululu.org{image}', image)
                # print(title_text_strip)
                # for val in comments[0:]:
                #     print(val.text.split('black')[0].split(')')[1])
                # print()

                for genre in find_genre[1:2]:
                    print(genre.find('a')['title'].split('-')[0])

        except requests.exceptions.HTTPError():
            raise Exception(response.url).with_traceback()

    return response


check_for_redirect()
