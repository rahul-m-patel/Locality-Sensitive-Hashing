import feedparser as fp
import json
from newspaper import Article
from time import mktime
from datetime import datetime

LIMIT = 10

newspapers = {}
#data['newspapers'] = {}

with open('NewsPapers.json') as data_file:
    companies = json.load(data_file)
    docID = 1
    for company,value in companies.items():
        count = 1
        d = fp.parse(value['rss'])
        newsPaper = {
            "rss" : value['rss'],
            "link" : value['link'],
            "articles" : []
        }
        for entry in d.entries:
            #print("HIII")
            #print(company)
            if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                article = {}
                article['DocID'] = docID
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                newsPaper['articles'].append(article)
                print(count, "articles downloaded from", company, ", url: ", entry.link)
                count = count + 1
                docID = docID + 1
        newspapers[company] = newsPaper
try:
    with open('scraped_articles.json', 'w') as outfile:
        json.dump(newspapers, outfile)
except Exception as e: print(e)
