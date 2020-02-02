import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

headers = {'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
          }

proxies = {
    'https': 'https://cG8A3e:YxUDzu@45.133.224.68:8000'
}

def write_csv(data):
    with open('yandex_dzen.csv', 'a', encoding='utf-8') as f:
        order = ['title', 'url1', 'description', 'auditory', 'subs']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def get_page_data(base_url):
    r = requests.get(base_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, 'lxml')
    channels_list = soup.find('div', class_='channels-list').find_all('div', class_='channel-item')
    for channel in channels_list:
        title = channel.find('a', class_='channel-item__link').text.strip()
        url = channel.find('a', class_='channel-item__link').get('href').strip()
        description = channel.find('p', class_='channel-item__description').text.strip()
        url1 = 'https://zen.yandex.ru' + url
        r1 = requests.get(url1, headers=headers, proxies=proxies)
        soup1 = BeautifulSoup(r1.text, 'lxml')
        divs = soup1.find_all('div', class_='channel-info-view__value')
        try:
            auditory = divs[0].text
        except:
            auditory = ''
        try:
            subs = divs[1].text
        except:
            subs = ''
        data = {
           'title': title,
            'url1': url1,
            'description': description,
            'auditory': auditory,
            'subs': subs
        }
        write_csv(data)

def main():
    base_urls = []
    for i in range(1, 13117):
        base_url = f'https://zen.yandex.ru/media/zen/channels?page={i}'
        base_urls.append(base_url)
    with Pool(100) as p:
        p.map(get_page_data, base_urls)

if __name__ == '__main__':
    main()