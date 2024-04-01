import requests
from bs4 import BeautifulSoup
import json
import time


# health tech newspaper
url = 'https://htn.co.uk/elementor-4910/'

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

arc_container = soup.select('.elementor-widget-container')

# print(type(arc_container[0]))


# soup = BeautifulSoup(page.text, "html.parser")
articles = []
for l in arc_container[0].find_all('a'):
    article = dict()
    article['title'] = l.string
    article['address'] = l.get('href')

    articles.append(article)

count = 0
for article in articles:
    article_page = requests.get(article['address'])
    soup_ = BeautifulSoup(article_page.text, "html.parser")
    content = soup_.find("div", {"class":"entry-content"})
    
    try:
        article['content'] = content.text
        count += 1
        print(f'Article {count}\'s content is scrapped out of {len(articles)} articles.')   
    except AttributeError:
        print("AttributeError") 

    if count % 10 == 0:
        time.sleep(7)
    
    if count == 200:
        break


# print(articles)

# Serializing json
json_object = json.dumps(articles)
 
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
