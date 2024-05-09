from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import requests

def get_page_data(url, tag):
    url_res = urlsplit(url)
    url_tuple = tuple(url_res)
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html5lib')
    tag_titles = []
    tag_titles_text = []
    for tag in soup.find_all(f'{tag}'):
        tag_titles.append(tag)
        tag_titles_text.append(tag.getText())
    return url_tuple, tag_titles, tag_titles_text


url = input('Введите url-адрес: ')
url_tuple, h1_titles, h1_titles_text = get_page_data(url, 'h1')

main_page_url = url.split('/')[0] + '//' + url.split('/')[2]
url_tuple_split, h2_titles, h2_titles_text = get_page_data(main_page_url, 'h2')

print('Исходный адрес: ', url, '\n', url_tuple, '\n', h1_titles, '\n', h1_titles_text)
print('Новый адрес: ', main_page_url, '\n', url_tuple_split, '\n', h2_titles, '\n', h2_titles_text)