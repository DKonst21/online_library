import requests
import argparse
import sys
import time
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from parse_tululu import check_for_redirect
from urllib.parse import urljoin


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


def save_content(file_content, filename, folder):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    with open(file_path, 'wb') as file:
        file.write(file_content.content)


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    for book_number in range(args.start_id, args.end_id + 1):
        book_page_url = f"https://tululu.org/b{book_number}/"
        payload = {'id': book_number}
        try:
            book_page_response = requests.get(book_page_url)
            book_page_response.raise_for_status()
            check_for_redirect(book_page_response)

            book_description = parse_book_page(book_page_response, book_page_url)
            print(book_description)
            print(f'Заголовок: {book_number}. {book_description["title"]}\n\
                    Жанры: {book_description["book_genres"]}\n')

            book_cover_image = requests.get(book_description['book_cover_link'])
            book_cover_image.raise_for_status()
            check_for_redirect(book_cover_image)
            save_content(book_cover_image, book_description['book_cover_filename'], folder='images/')

            book_text_response = requests.get(book_description['book_text_link'], params=payload)
            book_text_response.raise_for_status()
            check_for_redirect(book_text_response)
            save_content(book_text_response, book_description['book_text_filename'], folder='books/')

        except requests.HTTPError:
            print(f'Книга с id {book_number} не найдена...\n', file=sys.stderr)
            continue
        except requests.ConnectionError:
            print('Соединение с сайтом прервано, пробую продолжить работу...')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
