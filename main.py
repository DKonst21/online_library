import requests
import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from tululu import download_txt, download_image, parse_book_page, get_comments
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
    parser.add_argument('-end', '--end_id', type=int, default=11, help='Конечный номер')
    return parser


def parsing_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text.split('::')
    title_text_strip = title_text[0].strip()
    return title_text_strip


# def parsing_book_comments(response):
#     soup = BeautifulSoup(response.text, 'lxml')
#     comments = soup.find_all(class_='texts')
#     return comments


def parsing_book_genre(response):
    soup = BeautifulSoup(response.text, 'lxml')
    find_genre = soup.find_all(class_='d_book')
    return find_genre


# def get_slice_books(start, end):
#     for number_books in range(start, end):
#         url = f'https://tululu.org/b{number_books}/'
#         response = requests.get(url)
#         response.raise_for_status()
#     return response


def get_join_url():
    soup = BeautifulSoup(response.text, 'lxml')
    return urljoin('https://tululu.org', soup.find(class_='bookimage').find('img')['src'])


def get_responce(url):
    response = requests.get(url, allow_redirects=False)
    try:
        if response.status_code:
            print(response.history)
            return response
    except requests.exceptions.HTTPError():
        raise Exception(response.url).with_traceback()


def main():
    Path("books").mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    main()
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    for number_book in range(args.start_id, args.end_id):
        url = f'https://tululu.org/b{number_book}/'
        response = get_responce(url)

        # parsing_book_comments(response)
        parsing_book_genre(response)
        if check_for_redirect(response):
            download_txt(url, parsing_page(response))

            image = unquote(urlparse(get_join_url()).path)
            download_image(f'https://tululu.org{image}', image)
            #
            # parse_book_page(title_text, parsing_book_genre(response))
            # get_comments(comments)

