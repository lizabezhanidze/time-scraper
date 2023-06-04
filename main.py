import csv
import time
import requests
from bs4 import BeautifulSoup

INTERVAL = 5
URL = 'https://time.com/'
r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')

articles = {}

# time.com-ზე არსებული sidebar-ის ლინკებს ეძებს და თითოეული მათგანის პირველი პარაგრაფი მოაქვს
feed = soup.select_one('div.most-popular-feed-wrapper > ul')
for item in feed.select('li'):
    link = item.div.select('a')[1]
    title = link.get_text(strip=True)
    print(f'Scraping Article: "{title}"')
    response = requests.get(link['href'])
    article_soup = BeautifulSoup(response.text, 'html.parser')
    first_paragraph = article_soup.select_one('#article-body p').get_text()
    articles[title] = f'{first_paragraph}\n[Read More: {link["href"]}]'
    time.sleep(INTERVAL)

with open('articles.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=articles.keys())
    writer.writeheader()
    writer.writerow(articles)
