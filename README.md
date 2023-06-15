# Скачиваем книги из онлайн библиотеки.

Скрипт для скачивания книг из онлайн библиотеки.

## Запуск
- Скачайте архив с кодом ([ссылка для скачивания](https://github.com/DKonst21/online_library)) и распакуйте его.
- Установите необходимые библиотеки
```
python3 -m pip install -r requirements.txt
```
- Запустите сайт командой:
```
python main.py
```
По умолчанию скрипт скачает книги с id-номерами с первого по десятый. Для изменения стандартного поведения скрипта нужно запустить команду вида:
```
 python main.py -start 20 -end 30
```
где 20 и 30 - начальное и конечное значение диапозона id-номеров скачиваемых книг.

## Вспомогательные файлы

### tululu.py
Содержит следующие функции, необходимые для работы скрипта:
- download_txt(). Функция для скачивания текстов книг;
- download_image(). Функция для скачивания обложек книг;
- parse_book_page(). Выводит в консоль название, автора и жанр книги;
- get_comments(). Выводит в консоль комментарии к книге, которые оставили пользователи на сайте.

### bs4_tutorial.py
Руководство по парсингу на примере блога Франка Сонеберга [ссылка на блог](https://www.franksonnenbergonline.com/blog/are-you-grateful/)


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
