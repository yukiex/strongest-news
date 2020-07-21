import os
import feedparser
import json

feed_list = [
    "https://feedurl.com"
]

rss = []
for url in feed_list:
    print(url)
    articles = feedparser.parse(url)
    for e in articles.entries:
        rss.append(e)

if (os.path.exists('news_article.json')):
    rss_not_exist = []
    exist_article_ids = []  # 重複チェックのため
    with open('article.json') as f:
        exist_json = json.load(f)
    for article in rss:
        exist_flg = False
        for exist_article in exist_json:
            exist_article_ids.append(exist_article["id"])
            if (article["id"] in exist_article_ids):
                exist_article_ids.append(article["id"])
                exist_flg = True
                break
            exist_article_ids.append(article["id"])
        if(exist_flg == False):
            rss_not_exist.append(article)
    rss.extend(rss_not_exist)

fw = open('news_article.json', 'w')
json.dump(rss, fw, indent=4, ensure_ascii=False)
