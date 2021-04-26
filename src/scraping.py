import requests
import codecs
from bs4 import BeautifulSoup as Bs
from random import randint

# __all__ = ('hh', 'work_city')

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
    resp = requests.get(url, headers=header[randint(0, 2)])
    jobs = []
    if url:
        if resp.status_code == 200:
            soup = Bs(resp.content, 'html.parser')
            main_list = soup.find('div', attrs={'class': 'vacancy-serp'})
            if main_list:
                list_list = main_list.find_all('div', class_='vacancy-serp-item')
                for list in list_list:
                    title = 'text'
                    t = list.find('div', class_='vacancy-serp-item__row vacancy-serp-item__row_header')
                    if t:
                        title = t.a.text
                    title_url = t.a['href']
                    description = list.find('div', attrs={'class': 'g-user-content'}).text
                    company = 'No name'
                    c = list.find('div', class_='vacancy-serp-item__meta-info-company')
                    if c:
                        company = c.a.text
                    jobs.append({
                        'title': title, 'url': title_url,
                        'description': description, 'company': company,
                    })
    return jobs


# def work_city(url):
#     resp = requests.get(url, headers=header[randint(0, 2)])
#     jobs = []
#     if url:
#         if resp.status_code == 200:
#             soup = Bs(resp.content, 'html.parser')
#             main_Table = soup.find('div', attrs={'class': 'result-list'})
#             if main_Table:
#                 Table_list = main_Table.find_all('div', class_='snippet__inner')
#                 for Table in Table_list:
#                     title = Table.find('h2')
#                     title_url = title.a['href']
#                     description = Table.find('div', class_='snippet__desc').text
#                     company = Table.find('li', class_='snippet__meta-item snippet__meta-item_company').text
#                     jobs.append({
#                         'title': title.text, 'url': title_url,
#                         'description': description, 'company': company,
#                     })
#     return jobs


# if __name__ == '__main__':
#     # h.close()
#     print(hh('https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'))
#     print(work_city('https://moskva.gorodrabot.ru/python'))
