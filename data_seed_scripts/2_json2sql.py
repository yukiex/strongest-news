import json
import re
import emoji

with open('news_article.json') as f:
    df = json.load(f)

count = 0
sql = ""
for t in df:
    try:
        links = t["links"]
        img_url = ""
        for rel in links:
            if (rel["rel"] == "enclosure"):
                img_url = rel["href"]
        dt_p = t["published_parsed"]
        try:
            type_str = t["tags"][0]["term"]
        except Exception as err:
            type_str = "未分類"
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
                            "]+", flags=re.UNICODE)
        def remove_emoji(src_str):
            return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)
        _dt = ("{:0>2}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2}").format(dt_p[0],dt_p[1],dt_p[2],dt_p[3],dt_p[4],dt_p[5])
        sql += "INSERT INTO articles (id,title,detail,type,img_url,created_at,updated_at) VALUES ({},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");\n".format(
            str(count),
            t["title"].replace("'",""),
            remove_emoji(emoji_pattern.sub(r'@emoji', t["summary"].replace("'","").replace("\u3000","").replace("\"","\\\"").replace("\n",""))),
            type_str.replace("'",""),
            img_url,
            _dt,
            _dt
        )
        count += 1
    except Exception as e:
        print(e)

with open('2_articles.sql', 'w') as f:
    f.write(sql)