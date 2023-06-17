import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs('{}'.format(folder), exist_ok=True)
    split_name = filename.split('.')
    name = sanitize_filename(f'{split_name[0]}.txt')
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


def get_book_genre(response):
    soup = BeautifulSoup(response.text, 'lxml')
    genre = soup.find_all(class_='d_book')
    return genre


def printing_book_data(title_text, genres):
    print(f'Название: {title_text[0].strip()}')
    print(f'Автор: {title_text[1].strip()}')

    for genre in genres[1:2]:
        print(genre.find('a')['title'].split('-')[0])
    print()


def get_comments(comments):
    for val in comments[0:]:
        print(val.text.split('black')[0].split(')')[1])
    print()
