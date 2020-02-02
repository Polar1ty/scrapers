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
    with open('yandex_dzen_single_channel.csv', 'a', encoding='utf8') as f:
        order = ['title', 'href', 'views', 'views_till_end', 'percent', 'avg', 'date']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def get_page_data(link):
    r = requests.get(link, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, 'lxml')
    feedrows = soup.find_all('div', class_='feed__row')
    for feedrow in feedrows:
        cards = feedrow.find_all('div', class_='feed__item-wrap _size_small')
        for single_card in cards:
            try:
                href = single_card.find('a', class_='card-image-view__clickable').get('href')
            except:
                pass
            r1 = requests.get(href, headers=headers, proxies=proxies)
            soup1 = BeautifulSoup(r1.text, 'lxml')
            try:
                title = soup1.find('h1', class_='article__title').text
            except:
                title = ''
            try:
                date = soup1.find('meta', itemprop='datePublished').get('content')
            except:
                date = ''
            link = str(soup1.find('link', rel='canonical').get('href')).split('-')[-1]
            link_vsyakaya_hernya = f'https://zen.yandex.ru/media-api/publication-view-stat?publicationId={link}'
            r2 = requests.get(link_vsyakaya_hernya, headers=headers, proxies=proxies)
            soup2 = BeautifulSoup(r2.text, 'lxml')
            try:
                views = soup2.find('p').text.split(',')[1].split(':')[1]
            except:
                views = ''
            try:
                views_till_end = soup2.find('p').text.split(',')[2].split(':')[1]
            except:
                views_till_end = ''
            try:
                sum = soup2.find('p').text.split(',')[3].split(':')[1]
            except:
                sum = ''
            try:
                avg = round((int(sum)/int(views))/60, 2)
            except:
                avg = ''
            try:
                percent = str(round((int(views_till_end) * 100)/int(views), 2)) + '%'
            except:
                percent = ''
            data = {
                'title': title,
                'href': href,
                'views': views,
                'views_till_end': views_till_end,
                'percent': percent,
                'avg': avg,
                'date': date
            }
            print(data)

def main():
    mores = []
    links = []
    base_url = 'https://zen.yandex.ru/travelmaniac'
    r = requests.get(base_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, 'lxml')
    feedrows = soup.find_all('div', class_='feed__row')
    for feedrow in feedrows:
        cards = feedrow.find_all('div', class_='feed__item-wrap _size_small')
        for single_card in cards:
            try:
                href = single_card.find('a', class_='card-image-view__clickable').get('href')
            except:
                pass
    if href not in links:
        links.append(href)
    first_more = str(str(soup.find('body').find('script')).split('"more":"')[1].split('","')[0])
    def f(first_more):
        r = requests.get(first_more, headers=headers, proxies=proxies)
        try:
            more = r.json()['more']['link']
            mores.append(more)
            f(more)
        except KeyError:
            pass
    f(first_more)
    print(mores)
    print(len(mores))
    for m in mores:
        r = requests.get(m, headers=headers, proxies=proxies)
        for i in range(0, 20):
            try:
                link = r.json()['items'][i]['link']
                links.append(link)
            except:
                pass
    print(links)
    print(len(links))
    for link in links:
        get_page_data(link)
    # with Pool(100) as p:
    #     p.map(get_page_data, base_urls)

if __name__ == '__main__':
    main()