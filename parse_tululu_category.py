import argparse
import logging
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as BS

from main import check_for_redirect


def parse_book_links(category_page_response, category_page_url):
    category_page_soup = BS(category_page_response.text, 'lxml')
    all_books_selector = '.d_book'
    all_books_id = category_page_soup.select(all_books_selector)
    book_links_per_page = [urljoin(category_page_url, book_id.a['href']) for book_id in all_books_id]
    return book_links_per_page


def check_for_errors(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.HTTPError:
                err_statistics.append(args[0])
                break
            except requests.ConnectionError:
                print('\nПохоже соединение с сайтом прервано, пробую продолжить работу...', file=sys.stderr)
                time.sleep(10)
    return wrapper


@check_for_errors
def get_category_response(category_page_url):
        category_page_response = requests.get(category_page_url)
        category_page_response.raise_for_status()
        check_for_redirect(category_page_response)
        return category_page_response


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    book_urls = []
    book_descriptions = []
    err_statistics = []

    parser = argparse.ArgumentParser(
        description='''Скрипт предназначен для скачивания книг и их обложек с сайта "tululu.org" из раздела "фантастика".'''
    )
    parser.add_argument('--start_page', nargs='?', type=int, default=1,
                        help='Номер начальной страницы | First page\'s id')
    parser.add_argument('--end_page', nargs='?', type=int, default=702,
                        help='Номер финальной страницы | Last page\'s id')
    args = parser.parse_args()