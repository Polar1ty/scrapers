import requests
from bs4 import BeautifulSoup
import csv
import re

headers = {'Accept': '*/*',
    #'Cookie': '18dcbc98e575b729af454d0caf6716b5=87ad3bec9899b2b87f0aebdc690f7b93; _ga=GA1.2.781270232.1573144313; _gid=GA1.2.1780543975.1573144313; __utmc=170783009; __utmz=170783009.1573144313.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=6eda1535ff77acb82d86c9cb9faf0a01; perspektywy_cookies=1; cookies_accepted=T; grey_wizard_captcha=fJSW1k2NqP0YCF%2FjYAOf0QUD7%2BpqYbMFeHHtzOAsVrRW3do41xIoeQsldjYkLolVcE0zPPTLqakxDe2PMaQZBlr7JonlkcGiykC%2FZpvZ3vSU3XAhgtuEk%2BLkjRQtiJd6; grey_wizard=QQVS%2Blq5BeWMKVSp%2F%2ByktpSWVYxyYc4QqyIbzgKswiRcpWTcU5VAmPgUlPqsPcEdfhLcFCGHxHBGRCThncG0iGB5HkM26XFSwryY3nnNduC4BDUf6EPc736A7kPqgplU; __utma=170783009.781270232.1573144313.1573203950.1573207778.6; __utmt=1; __utmb=170783009.2.10.1573207778',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
          }

proxies = {
    'http': 'http://cG8A3e:YxUDzu@45.133.224.68:8000'
}


def write_csv(data):
    with open('perspektywy_again.csv', 'a', encoding='utf8') as f:
        order = ['title', 'faculty', 'department', 'direction', 'speciality', 'ajax']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def get_page_data(base_url):
    r = requests.get(base_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        title = soup.find('table', id='uczelnia_dane').find('h2').text
    except:
        pass
    try:
        megabaza = soup.find('div', id='megabaza').find_all('div', class_='uczelnia')
        for div in megabaza:
            try:
                faculty = div.find('h2', class_='nazwa').text
            except:
                pass
            try:
                ul = div.find('ul', class_='studia').find_all('li')
            except:
                pass
            try:
                for li in ul:
                    try:
                        script = str(li.find('script', type='text/javascript'))
                        id = re.findall('\d{5}', script)[0]
                        print(id)
                        url = f'http://www.perspektywy.pl/portal/megabaza/wyszukiwarka_szcz/zasady_przyjec.php?idStudia={id}'
                        r1 = requests.get(url, headers=headers, proxies=proxies)
                        soup1 = BeautifulSoup(r1.text, 'lxml')
                        ajax = soup1.find_all('div')[1].text
                    except:
                        pass
                    try:
                        department = li.find('div', class_='opis_left').find('p').find('a').text.strip()
                    except:
                        pass
                    try:
                        speciality = li.find('div', class_='opis_left').find('p').text.strip()
                        if str(department) == str(speciality):
                            speciality = ''
                        else:
                            speciality = li.find('div', class_='opis_left').find('p').text.strip()
                    except:
                        pass
                    try:
                        direction = li.find('div', class_='opis_left').find_all('p')[1].text.strip()
                    except:
                        pass
                    data = {
                        'title': title,
                        'department': department,
                        'faculty': faculty,
                        'speciality': speciality,
                        'direction': direction,
                        'ajax': ajax
                    }
                    write_csv(data)
            except:
                pass
    except:
        pass

def main():
    base_urls = []
    try:
        for i in range(1, 1000):
            base_url = f'http://www.perspektywy.pl/portal/index.php?option=com_content&view=article&id=3&Itemid=114&id_uczelnia={i}'
            base_urls.append(base_url)
    except:
        pass
    for url in  base_urls:
        get_page_data(url)
        print(url)


if __name__ == '__main__':
    main()

