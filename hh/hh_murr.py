import urlib.requests
response = urlib
import csv as cvs_
from bs4 import BeautifulSoup as bs

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'

base_url = 'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=%D0%9F%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA+%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0&page=0'


def hh_parse(base_url, headers):
    jobs = []
    urls =[]
    urls.append(base_url)
    session = rq.Session()
    requests = session.get(base_url, headers=headers)
    if requests.status_code == 200:
        soup = bs(requests.content,  'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=%D0%9F%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA+%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0&page={i}'
                if url not in urls:
                    urls.append(url)
                print(url)
        except:
            pass
        for url in urls:
            requests = session.get(base_url, headers = headers)
            soup = bs(requests.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa' : 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                content = text1 + ' ' + text2
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'content': content
                })
            except:
                pass

            print(len(jobs))

    else:
        print('ERROR or Done' + str(requests.status_code))
    return jobs

def files_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Name of vacancy', 'URL', 'Name of company', 'Description'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))

jobs = hh_parse(base_url, headers)
files_writer(jobs)
