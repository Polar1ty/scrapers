import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import uniform
import re
import pandas as pd

headers = {'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
          }

proxies = {
    'https': 'https://cG8A3e:YxUDzu@45.133.224.68:8000'
}

def write_csv(data):
    with open('joblab.csv', 'a', encoding='utf-8') as f:
        order = ['email']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

def get_page_data(base_url):
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        ps = soup.find('td', class_='contentmain').find_all('p', class_='prof')
        for p in ps:
            part_of_url = str(p.find('a').get('href'))
            joblab = 'https://joblab.ru'
            vac_url = joblab + part_of_url

            random_integer = uniform(4, 8)
            ua = dict(DesiredCapabilities.CHROME)
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x935')
            driver = webdriver.Chrome(chrome_options=options)
            time.sleep(random_integer)

            try:
                driver.get(vac_url)
                time.sleep(random_integer)
                driver.find_element_by_xpath('//*[@id="m"]/a').click()
                time.sleep(random_integer)
                email = driver.find_elements_by_xpath('//*[@id="m"]/a')
                time.sleep(random_integer)
                for x in email:
                    final_email = x.text
                    data = {
                        'email': final_email
                            }
                    print(x.text)
                    write_csv(data)
                time.sleep(random_integer)
                driver.quit()
                time.sleep(random_integer)
            except:
                time.sleep(random_integer)
                driver.quit()
                time.sleep(random_integer)
    except:
        pass


def main():
    base_url = 'https://joblab.ru/search.php?r=vac&srcategory=12&submit=1'
    #base_url = input('Введите вашу ссылку:')
    while True:
        get_page_data(base_url)
        r = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            pattern = 'Следующая →'
            base_url = 'https://joblab.ru' + soup.find('a', text=re.compile(pattern)).get('href')
            print(base_url)
        except:
            break
    print('Парсинг успешно завершён')
    input('Press ENTER to exit')
    df = pd.read_csv('joblab.csv')
    modified_df = df.dropna(how='all')
    modified_df.to_csv('joblab_rewrited.csv', index=False)


if __name__ == '__main__':
    main()