import requests
import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from tululu import download_txt, download_image
from urllib.parse import urljoin, unquote, urlparse


def check_for_redirect(response):
    try:
        if not response.history:
            return response
    except requests.exceptions.HTTPError():
        raise Exception(response.url).with_traceback()


def create_parser():
    parser = argparse.ArgumentParser(
        description='''Скрипт имеет два необязательных аргумента: 
                    --start - начальный id-номер скачиваемой книги; 
                    --end - конечный id-номер. 
                    По умолчанию скачиваются книги с id-номерами с первого по десятый включительно.'''
    )
    parser.add_argument('-start', '--start_id', type=int, default=1, help='Начальный номер')
    parser.add_argument('-end', '--end_id', type=int, default=10, help='Конечный номер')
    return parser


def download_text_book(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text.split('::')
    title_text_strip = title_text[0].strip()
    return title_text_strip


def get_join_url():
    soup = BeautifulSoup(response.text, 'lxml')
    directory = soup.find(class_='bookimage').find('img')['src'].split('/')[1]
    return urljoin(f'https://tululu.org{directory}', soup.find(class_='bookimage').find('img')['src'])


def get_responce(url):
    response = requests.get(url, allow_redirects=False)
    try:
        if response.status_code:
            return response
    except requests.exceptions.HTTPError():
        raise Exception(response.url).with_traceback()


def main():
    try:
        Path("books").mkdir(parents=True, exist_ok=True)
    except requests.exceptions.ConnectionError:
        """A Connection error occurred."""


if __name__ == '__main__':
    main()
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    for book_number in range(args.start_id, args.end_id+1):
        url = f'https://tululu.org/b{book_number}/'
        url_text_book = f'https://tululu.org/txt.php?id={book_number}/'
        response = get_responce(url)

        if check_for_redirect(response):
            download_txt(url_text_book, download_text_book(response))
            image = unquote(urlparse(get_join_url()).path)
            download_image(f'https://tululu.org{image}', image)
