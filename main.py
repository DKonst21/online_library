import requests
import argparse
import sys
import time
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from parse_tululu import download_txt, download_image, check_for_redirect
from urllib.parse import urljoin, unquote, urlparse


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


def parse_book_page(book_page_response, book_page_url):
    bookpage_soup = BeautifulSoup(book_page_response.text, 'lxml')

    text_link_selector = 'table.d_book a'
    book_text_link = urljoin(book_page_url, bookpage_soup.select(text_link_selector)[-3]['href'])
    if '_votes' in book_text_link:
        raise requests.HTTPError()

    title_selector = 'h1'
    title, author = bookpage_soup.select(title_selector)[0].text.split('::')
    title = title.strip()

    genre_selector = 'span.d_book a'
    genres = bookpage_soup.select(genre_selector)
    book_genres = [genre.text for genre in genres]

    comments_selector = '.texts span.black'
    comments = bookpage_soup.select(comments_selector)
    book_comments = [comment.text for comment in comments]

    book_cover_selector = '.bookimage img'
    book_cover = bookpage_soup.select(book_cover_selector)[0]['src']
    book_cover_link = urljoin(book_page_url, book_cover)
    book_cover_filename = book_cover.split('/')[2]

    book_text_filename = sanitize_filename(title).replace(' ', '_')

    book_description = {
        'title': title,
        'author': author.strip(),
        'book_cover_link': book_cover_link,
        'book_cover_filename': book_cover_filename,
        'book_text_filename': f'{book_text_filename}.txt',
        'book_text_link': book_text_link,
        'book_genres': book_genres,
        'book_comments': book_comments,
    }
    return book_description


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
