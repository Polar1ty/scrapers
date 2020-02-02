import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

headers = {'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
          }

proxies = {
    'https': 'https://cG8A3e:YxUDzu@45.133.224.68:8000'
}

def write_csv(data):
    with open('hh.csv', 'a', encoding='utf-8') as f:
        order = ['title', 'email']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def get_page_data(base_url):
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    item_vacs = soup.find_all('div', class_='vacancy-serp-item')
    for item_vac in item_vacs:
        title = item_vac.find('a', class_='bloko-link HH-LinkModifier').text
        print(title)
        try:
            script = str(item_vac.find('span', class_='bloko-link bloko-link_dimmed'))
            id = re.findall('\d{8}', script)[0]
            emploer_id = script.split(':')[2].split(',')[0].strip()
            show_contacts = f'https://hh.ru/vacancy/{id}/contacts?employerId={emploer_id}'
            r = requests.get(show_contacts, headers=headers)
            email = r.json()['email']
            print(email)
            data = {
                'title': title,
                'email': email
            }
            write_csv(data)
        except:
            pass

def main():
    base_url = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BD%D0%B8%D0%BA+%D1%81%D0%BA%D0%BB%D0%B0%D0%B4%D0%B0'
    #base_url = input('Введите вашу ссылку:')
    get_page_data(base_url)
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    next_page = 'https://hh.ru/' + soup.find('a', class_='bloko-button HH-Pager-Controls-Next HH-Pager-Control').get('href')
    def pagination(next_page):
        try:
            get_page_data(next_page)
            r = requests.get(next_page, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            next_page = 'https://hh.ru/' + soup.find('a', class_='bloko-button HH-Pager-Controls-Next HH-Pager-Control').get('href')
            pagination(next_page)
        except:
            print('Парсинг завершен успешно')
    pagination(next_page)
    df = pd.read_csv('hh.csv')
    modified_df = df.dropna(how='all')
    modified_df.to_csv('hh_rewrited.csv', index=False)

if __name__ == '__main__':
    main()