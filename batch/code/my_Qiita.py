import requests
import json
import pprint
import time
from my_tools import calc_distance
#from my_tools import calc_distance

def getQiitaInfo(query, per_page):
    token = "5798518994eec676de3272cc9c15405cf3b697d5"
    headers = {
        "Authorization": "Bearer " + token
    }
    params = {
        "query" : f'{query}',
        "page": "1",
        "per_page": per_page,
    }
    res = requests.get('https://qiita.com/api/v2/items', params=params, headers=headers)
    jsondata = json.loads(res.text)
    return jsondata






def getQiitaTags(tag_name):
    def getAllQiitaTag():
        token = "5798518994eec676de3272cc9c15405cf3b697d5"
        headers = {
            "Authorization": "Bearer " + token
        }
        origin = []
        for i in range(0, 2):
            params = {
                "page": i+1,
                "per_page": "100",
                "sort" : "count"
            }
            res = requests.get('https://qiita.com/api/v2/tags', params=params, headers=headers)
            jsondata = json.loads(res.text)
            time.sleep(1)
            return jsondata
    
    all_qiita_tags = getAllQiitaTag()
    for row in all_qiita_tags:
        if (row["id"] == tag_name):
            return row
    return list(sorted(all_qiita_tags, key=lambda x: calc_distance(x["id"], tag_name) ))[0]



import requests
import json
import datetime
import pytz

BASE_URL = "https://qiita.com/api/v2/items"

def putQiitaArticle(title = "フレームワーク/プログラミング言語 ランキングTop15", markdown = "test", tags = [{"name": "flamevalue"}], path="article", id="",  is_private=False):
    #token = "5a92018081a8bb606ec0cb199360a581548bd235"
    token = "3e081afb9ee5b72d69f63cb3d69e0889b491a627"
    headers = {"Authorization": f"Bearer {token}"}
    item = {
        "title": title,
        "id": id,
        "tags": tags,
        "private": is_private,
        "coediting": False,
        "tweet": False,
        "body": markdown
    }
    print("【Log】【Qiita】 execute putQiitaArticle")
    # idがなければ、新規で記事を投稿
    if item["id"] == "":
        res = requests.post(BASE_URL, headers=headers, json=item)
        return res
    else:
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        item["title"] += now.strftime("【%Y/%m/%d %H:%M更新】")
        item_id = item["id"]
        res = requests.patch(BASE_URL + f"/{item_id}", headers=headers, json=item)
        return res




if __name__ == "__main__":
    res = putQiitaArticle("この記事はQiitaから投稿しています", "#test " ,"article", "c2acb400a27ab78c22b6").json()
    print(res)




