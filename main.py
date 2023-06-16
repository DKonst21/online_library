import requests
import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from tululu import download_txt, download_image, parse_book_page, get_comments
from urllib.parse import urljoin, unquote, urlparse


def check_for_redirect(start, end):
    for number_books in range(start, end):
        url = f'https://tululu.org/b{number_books}/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('h1')
        title_text = title_tag.text.split('::')
        title_text_strip = title_text[0].strip()
        comments = soup.find_all(class_='texts')
        find_genre = soup.find_all(class_='d_book')

        try:
            if response.history == []:

                download_txt(url, title_text_strip)

                image = unquote(urlparse(
                    urljoin('https://tululu.org', soup.find(class_='bookimage').find('img')['src'])).path)
                download_image(f'https://tululu.org{image}', image)

                parse_book_page(title_text, find_genre)
                get_comments(comments)

        except requests.exceptions.HTTPError():
            raise Exception(response.url).with_traceback()

    return response


def create_parser():
    parser = argparse.ArgumentParser(
        description='''Скрипт имеет два необязательных аргумента: 
                    --start - начальный id-номер скачиваемой книги; 
                    --end - конечный id-номер. 
                    По умолчанию скачиваются книги с id-номерами с первого по десятый включительно.'''
    )
    parser.add_argument('-start', '--start_id', type=int, default=1, help='Начальный номер')
    parser.add_argument('-end', '--end_id', type=int, default=11, help='Конечный номер')
    return parser


def main():
    Path("books").mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    main()
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    for _ in range(args.start_id):
        start = args.start_id
        end = args.end_id+1
    check_for_redirect(start, end)
