import requests
import os
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError()


def download_txt(url, book_title, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    os.makedirs('{}'.format(folder), exist_ok=True)
    split_name = book_title.split('.')
    name = sanitize_filename(f'{split_name[0]}.txt')
    path = os.path.join(folder, name)

    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def download_image(url, path_image, folder='image/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    os.makedirs('{}'.format(folder), exist_ok=True)
    split_name = path_image.split('/')
    name = sanitize_filename(f'{split_name[2]}')
    path = os.path.join(folder, name)
    
    with open(path, 'wb') as file:
        file.write(response.content)
    return path
