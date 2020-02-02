import requests
from bs4 import \
    BeautifulSoup  # для работы этой библеотеки пропишите в терминале -'pip install BeautifulSoup' и если потребуется -'pip install lxml'
import csv
from time import sleep
from random import randint

# скрипт работает на python 3.7

header = {'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

proxies = {
    #'https': '81.162.65.170:8080' ua
    #'https': '195.78.93.28:3128' ua
    #'https': '109.124.97.226:8080' Ru
    'https': '109.101.139.106:61139' # Romania
    #'https': '95.79.55.196:53281' # Ru
    #'https': '193.85.228.182:43036' # Czech2
    #'https': '176.98.76.203:51270' # Cool UA proxy
    #'https': '202.152.27.75:8080' # Indonezia
    #'https': '188.163.84.15:443' # Serega server
    #'https': '219.157.144.198:8118' # China
    #'https': '46.227.169.206:8888' # Czech
    #'https': '87.103.234.116:3128' ru
}


def write_csv(data):
    with open('flagma_ads.csv', 'a', encoding='utf8') as f:
        order = ['title', 'description_edited', 'number_of_ad', 'date', 'output_category_edited', 'city', 'company',
                 'name', 'position', 'company_url', 'phones', 'phones1', 'phones2']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_page_data(url):
    r = requests.get(url, headers=header, proxies=proxies)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'lxml')
    tops = soup.find_all('div', class_='page-list-item top highlight')
    basic = soup.find_all('div', class_='page-list-item')
    together = tops + basic
    for someone in together:
        try:
            random_number = randint(4, 7)
            url = someone.find('div', class_='page-list-item-header').find('div', class_='header').find('a').get(
                'href')
            sleep(random_number)
            r1 = requests.get(url, headers=header, proxies=proxies)
            soup1 = BeautifulSoup(r1.text, 'lxml')
            try:
                title = soup1.find('div', class_='header-price-container').find('h1').text
            except:
                title = ''
            print(title, r.status_code)
            try:
                description = soup1.find('div', id='description').find_all('p')
                description_edited = str(description).replace('<br/>', '').replace('<p>', '').replace('</p>',
                                                                                                      '').replace('\n',
                                                                                                                  '')
            except:
                description_edited = ''
            try:
                number_of_ad = soup1.find('div', class_='desc-bottom').find('div').text.strip().split()[2]
            except:
                number_of_ad = ''
            try:
                date = soup1.find('div', class_='updated').text
            except:
                date = ''
            try:
                categories = soup1.find('div', class_='bread-crumbs').find_all('span', itemprop='itemListElement')
                try:
                    for category in categories:
                        output_category = str(category.find('a').find('span', itemprop='name').text.strip())
                    output_category_edited = output_category.replace('\n', ',')
                except AttributeError:
                    pass
            except:
                output_category_edited = ''
            try:
                city = str(soup1.find('div', class_='seller').find('div', class_='company-info').find('span',
                                                                                                      class_='terr').text).split(
                    ',')[0]
            except:
                city = ''
            try:
                company = soup1.find('div', class_='seller').find('div', class_='company-info').find('a').find(
                    'span').text
            except:
                company = ''
            try:
                name = soup1.find('div', class_='seller').find('div', class_='user-name').find('span').text
            except:
                name = ''
            try:
                position = soup1.find('div', class_='seller').find('div', class_='user-position').find('span').text
            except:
                position
            try:
                company_url = soup1.find('div', class_='seller').find('div', class_='company-info').find('a').get(
                    'href')
            except:
                company_url = ''

            try:
                try:
                    phones = str(soup1.find('div', class_='phones').find_all('a'))[47:66]
                except:
                    phones = ''
                try:
                    phones1 = str(soup1.find('div', class_='phones').find_all('a'))[118:137]
                except:
                    phones1 = ''
                try:
                    phones2 = str(soup1.find('div', class_='phones').find_all('a'))[189:208]
                except:
                    phones2 = ''
            except:
                pass
            data = {'title': title,
                    'description_edited': description_edited,
                    'number_of_ad': number_of_ad,
                    'date': date,
                    'output_category_edited': output_category_edited,
                    'city': city,
                    'company': company,
                    'name': name,
                    'position': position,
                    'company_url': company_url,
                    'phones': phones,
                    'phones1': phones1,
                    'phones2': phones2}
            write_csv(data)
            #print(data)
        except:
            pass


def main():
    links_p = []
    #base_url = 'https://flagma.ua/s1/muka-eksport-uo1251774-130-{}.html'
    link1 = 'https://flagma.ua/s1/muka-eksport-uo1251774-130-1.html'
    r0 = requests.get(link1, headers=header, proxies=proxies)
    soup0 = BeautifulSoup(r0.text, 'lxml')
    count = int(soup0.find('ul', id='yw0').find('li', class_='page notactive').text)
    for i in range(1, count + 1):
        linkp = f'https://flagma.ua/s1/muka-eksport-uo1251774-130-{i}.html'
        if linkp not in links_p:
            links_p.append(linkp)
    #--------------------------------------------------------------------------------#
    link2 = 'https://flagma.ua/drevesina-bumaga-o-1.html'
    r0 = requests.get(link2, headers=header, proxies=proxies)
    soup0 = BeautifulSoup(r0.text, 'lxml')
    count = int(soup0.find('ul', id='yw0').find('li', class_='page notactive').text)
    for i in range(1, count + 1):
        linkp = f'https://flagma.ua/drevesina-bumaga-o-{i}.html'
        if linkp not in links_p:
            links_p.append(linkp)
    #------------------------------------------------------------------------------------#
    link3 = 'https://flagma.ua/produkty-pitaniya-o-1.html'
    r0 = requests.get(link3, headers=header, proxies=proxies)
    soup0 = BeautifulSoup(r0.text, 'lxml')
    count = int(soup0.find('ul', id='yw0').find('li', class_='page notactive').text)
    for i in range(1, count + 1):
        linkp = f'https://flagma.ua/produkty-pitaniya-o-{i}.html'
        if linkp not in links_p:
            links_p.append(linkp)
    #---------------------------------------------------------------------------------------#
    link4 = 'https://flagma.ua/oborudovanie-o-1.html'
    r0 = requests.get(link4, headers=header, proxies=proxies)
    soup0 = BeautifulSoup(r0.text, 'lxml')
    count = int(soup0.find('ul', id='yw0').find('li', class_='page notactive').text)
    for i in range(1, count + 1):
        linkp = f'https://flagma.ua/oborudovanie-o-{i}.html'
        if linkp not in links_p:
            links_p.append(linkp)
    #---------------------------------------------------------------------------------------------#
    link5 = 'https://flagma.ua/stroitelnye-materialy-o-1.html'
    r0 = requests.get(link5, headers=header, proxies=proxies)
    soup0 = BeautifulSoup(r0.text, 'lxml')
    count = int(soup0.find('ul', id='yw0').find('li', class_='page notactive').text)
    for i in range(1, count + 1):
        linkp = f'https://flagma.ua/stroitelnye-materialy-o-{i}.html'
        if linkp not in links_p:
            links_p.append(linkp)
    for link in links_p:
        get_page_data(link)


if __name__ == '__main__':
    main()
