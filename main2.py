from collections import OrderedDict

import requests
import matplotlib.pyplot as plt
from urllib.parse import urljoin
from bs4 import BeautifulSoup


url = 'https://www.bookvoed.ru'
url_catalog = 'https://www.bookvoed.ru/catalog'


def get_href(url, class_a, tag):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    url_title = []
    url_href = []
    for tag in soup.find_all(f'{tag}', class_=f'{class_a}'):
        url_title.append(tag.get_text())
        url_href.append(tag.get('href'))
    return url_title, url_href


def create_new_url(href, select_href):
    new_path = url + href[select_href]
    url_new = urljoin(url, new_path)
    return url_new


def find_and_get_index(data_list):
    for index, item in enumerate(data_list):
        if item.startswith('Год'):
            return index
    return -1


def filter_arr_find_year(book, ind):
    start_range = 0
    end_range = 0
    if book[ind].startswith('Год издания'):
        start_range = len(book[ind]) - 5
        end_range = len(book[ind]) - 1
    elif book[ind].startswith('Год производства'):
        start_range = len(book[ind]) - 5
        end_range = len(book[ind]) - 1
    else:
        start_range = 0
        end_range = 0
    return start_range, end_range


def sorted_list(count):
    sorted_count = dict(sorted(count.items()))
    return sorted_count


def filter_sum_year(year, url_b, count, titles):
    if year > 2014:
        book_titles, books_href = get_href(url_b, 'product-title-author__title', 'h1')
        titles.append(''.join(map(str, book_titles)))
        if year in count:
            count[year] += 1
        else:
            count[year] = 1
    sorted_count = sorted_list(count)
    return titles, sorted_count


def plot_book(book_list):
    year = list(book_list.keys())
    book_count = list(book_list.values())
    plt.figure(figsize=(10, 6))
    plt.plot(year, book_count, marker='o', linestyle='-')
    plt.xlabel('Год')
    plt.ylabel('Количество книг')
    plt.title('Количество книг по годам')
    plt.grid(True)
    plt.show()


baseurl_title, baseurl_href = get_href(url_catalog, 'catalog-navigation__item', 'a')
print('Исходный адрес: ', url, '\n', baseurl_title)
select_href_category = int(input('Выберете категорию(0-21): '))

url_category = create_new_url(baseurl_href, select_href_category)
catalog_title, catalog_href = get_href(url_category, 'product-description__link', 'a')
books_titles = []
year_count = {}
for i in range(0, len(catalog_title)):
    select_href_book = i
    url_book = create_new_url(catalog_href, select_href_book)
    text_book, href_book = get_href(url_book, 'product-characteristics-full__row', 'tr')
    index = find_and_get_index(text_book)
    year_edition_arr = []
    start_range_year, end_range_year = filter_arr_find_year(text_book, index)
    for j in range(start_range_year, end_range_year):
        year_edition_arr.append(text_book[index][j])
    if not year_edition_arr:
        year_edition = 0
    else:
        year_edition = int(''.join(map(str, year_edition_arr)))
    books_titles, year_count_sorted = filter_sum_year(year_edition, url_book, year_count, books_titles)

print('адрес: ', url_category, '\n', books_titles)
plot_book(year_count_sorted)