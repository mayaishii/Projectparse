import time
import requests
import csv

def take_1000_posts():

    token = 'e9f379e6e9f379e6e9f379e6b7e99dfdb4ee9f3e9f379e6b403aad124656f27084a1b59'
    version = 5.92
    domain = 'fatdogclub'
    count = 100
    offset = 0
    all_posts = []


    while offset < 1000:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': 100,
                                    'offset': offset
                                }
                                )
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
    return all_posts


def file_writer(data):
    with open('fatdogs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('likes', 'body', 'url'))
        for post in data:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                     img_url = 'pass'
            except:
                pass

            a_pen.writerow((post['likes']['count'], post['text'], img_url))

all_posts = take_1000_posts()
file_writer(all_posts)

print(1)