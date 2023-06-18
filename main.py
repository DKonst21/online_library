import requests
import argparse
import sys
import time
from pathlib import Path
from bs4 import BeautifulSoup
from parse_tululu import download_txt, download_image
from urllib.parse import urljoin, unquote, urlparse


def check_for_redirect(response):
    if not response.history:
        return response
    else:
        return requests.HTTPError()


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


def get_name_book(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text.split('::')
    title_text_strip = title_text[0].strip()
    return title_text_strip


def get_join_url(response):
    soup = BeautifulSoup(response.text, 'lxml')
    directory = soup.find(class_='bookimage').find('img')['src'].split('/')[1]
    return urljoin(f'https://tululu.org{directory}', soup.find(class_='bookimage').find('img')['src'])


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    for book_number in range(args.start_id, args.end_id + 1):
        url = f'https://tululu.org/b{book_number}/'
        payload = {"id": book_number}
        url_text_book = requests.get('https://tululu.org/txt.php', params=payload).url
        try:
            response = requests.get(url, allow_redirects=False)
            response.raise_for_status()
            check_for_redirect(requests.get(url_text_book, allow_redirects=False))
            download_txt(url_text_book, get_name_book(response))
            path_image = unquote(urlparse(get_join_url(response)).path)
            download_image(f'https://tululu.org{path_image}', path_image)

        except requests.HTTPError:
            print(f'Книга с id {book_number} не найдена...\n', file=sys.stderr)
            continue
        except requests.ConnectionError:
            print('Соединение с сайтом прервано, пробую продолжить работу...')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
