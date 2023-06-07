import requests
from pathlib import Path


Path("books").mkdir(parents=True, exist_ok=True)

for number_books in range(1,11):
    url = f'https://tululu.org/txt.php?id={number_books}'
    response = requests.get(url)
    response.raise_for_status()

    filename = f'books/id{number_books}.txt'
    with open(filename, 'wb') as file:
        file.write(response.content)
