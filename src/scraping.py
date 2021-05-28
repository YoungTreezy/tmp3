import requests
from bs4 import BeautifulSoup as Bs
from random import randint

# подключаем агентов чтоб бота не забанили
header = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,applications/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 2 XL Build/PPP3.180510.008) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
     'Accept': 'text/html,applications/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Version/4.0 Chrome/71.1.2222.33 Mobile Safari/537.36',
     'Accept': 'text/html,applications/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
]


def hh_parser(url):
    # задаем параметры какие url должны посещать агенты
    resp = requests.get(url, headers=header[randint(0, 2)])
    jobs = []
    # делает проверку есть ли url
    if url:
        # если статус = 200, то робот начинает собирать инфу
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            # ищет класс в котором находятся вакансии
            main_list = soup.find('div', attrs={'class': 'vacancy-serp'})
            if main_list:
                # собирает 10 первых записей
                list_list = main_list.find_all('div', class_='vacancy-serp-item', limit=10)
                for list in list_list:
                    # ищет title
                    title = 'text'
                    t = list.find('div', class_='vacancy-serp-item__row vacancy-serp-item__row_header')
                    if t:
                        title = t.a.text
                    # ищет urls
                    title_url = t.a['href']
                    # ищет descriptions
                    description = list.find('div', attrs={'class': 'g-user-content'}).text
                    # ищет названия компаний
                    company = 'No name'
                    c = list.find('div', class_='vacancy-serp-item__meta-info-company')
                    if c:
                        company = c.a.text
                    # словарь добавляется в список
                    jobs.append({
                        'title': title, 'url': title_url,
                        'description': description, 'company': company,
                    })
    # выводит список словарей
    return jobs


# if __name__ == '__main__':
#     print(hh_parser('https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'))
