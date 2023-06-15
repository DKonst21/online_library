import requests
import os
from pathvalidate import sanitize_filename


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs('{}'.format(folder), exist_ok=True)
    name_split = filename.split('.')
    name = sanitize_filename(f'{name_split[0]}.txt')
    path = os.path.join(folder, name)

    # with open(path, 'wb') as file:
    #     file.write(response.content)
    # return path


def download_image(url, filename, folder='image/'):
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs('{}'.format(folder), exist_ok=True)
    name_split = filename.split('/')
    name = sanitize_filename(f'{name_split[2]}')
    path = os.path.join(folder, name)
    
    # with open(path, 'wb') as file:
    #     file.write(response.content)
    # return path


def parse_book_page(title_text_strip, find_genre):
    print(f'Заголовок: {title_text_strip}')

    for genre in find_genre[1:2]:
        print(genre.find('a')['title'].split('-')[0])
    print()