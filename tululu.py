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

    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def download_image(url, filename, folder='image/'):
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs('{}'.format(folder), exist_ok=True)
    name_split = filename.split('/')
    name = sanitize_filename(f'{name_split[2]}')
    path = os.path.join(folder, name)
    
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def parse_book_page(title_text, find_genre):
    print(f'Название: {title_text[0].strip()}')
    print(f'Автор: {title_text[1].strip()}')

    for genre in find_genre[1:2]:
        print(genre.find('a')['title'].split('-')[0])
    print()

def get_comments(comments):
    for val in comments[0:]:
        print(val.text.split('black')[0].split(')')[1])
    print()