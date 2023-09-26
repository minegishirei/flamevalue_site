import json
from requests_oauthlib import OAuth1Session
import pprint
MAIN_KEYS = {
    'consumer_key':'kBAze00GyDfwYaz673itPtWHx',
    'consumer_secret':'gr5WuLP4mdCBedKyyva1PIYq7ylSU9Kicp3vC4fyAyjYyL3geD',
    'access_token':'968269222525587456-gYTZbY4ph179lrI8mZDPEWXnAubYIbr',
    'access_secret':'0BpC5rsM2VVGjteHJPm53nk8bzidGGMIAboWf5Dyk9P3J',
    'client_key' : "3rJOl1ODzm9yZy63FACdg",
    'client_secret':"5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"
}

SE_MAINTAIN_KEYS = {
    'consumer_key' : "HLWAbVyeMNJ4NLusYh4R0mhr1",
    'consumer_secret':"Hepu8c5cIApyooctbXoZSDBf6mJLEeRL15juRYCl3x7MHEUDf2",
    'access_token':'1349555933257469955-kxP5n4bT9xrMYLpp95nlFU7hszmbAj',
    'access_secret':'xqlZmlU5zUWzCeuOyqDlDn3TNi8p7evlQMF60WWzqD18B',
}


class MyTwitterException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyTwitterAction():
    def __init__(self, KEYS = MAIN_KEYS):
        self.KEYS = KEYS
        print(self.KEYS)
        self.twitter = OAuth1Session(
            KEYS['consumer_key'],
            KEYS['consumer_secret'],
            KEYS['access_token'],
            KEYS['access_secret'])

    def search_tweet_list(self, q, amount):
        params = {
            "q" : q,
            #'q' : "仕事" + " since:20{}-{}-{}_00:00:00_JST min_faves:1000".format(year,month,day),  #検索文字列
            #'q' : "あけ since:2018-12-31_23:59:59_JST until:2019-01-01_00:00:00_JST",
            'count': amount
        }
        url = "https://api.twitter.com/1.1/search/tweets.json"
        req = self.twitter.get(url, params = params)
        print(req)
        if req.status_code == 200:
            tweet = json.loads(req.text)
            search_timeline = json.loads(req.text)
        else:
            raise MyTwitterException(req)
        return search_timeline['statuses']

    def search_popular_tweet_list(self, q, amount):
        params = {
            "q" : q,
            "result_type" : "popular",
            'count': amount
        }
        url = "https://api.twitter.com/1.1/search/tweets.json"
        req = self.twitter.get(url, params = params)
        print(req)
        if req.status_code == 200:
            tweet = json.loads(req.text)
            search_timeline = json.loads(req.text)
        else:
            raise MyTwitterException(req)
        return search_timeline['statuses']

    def search_retweet(self, tweet_id, count):
        params = {
            "id" : tweet_id,
            "count" : count
        }
        url = f"https://api.twitter.com/1.1/statuses/lookup.json?id={tweet_id}"
        req = self.twitter.get(url, params = params)
        print(req)
        if req.status_code == 200:
            tweet = json.loads(req.text)
            search_timeline = json.loads(req.text)
        else:
            raise MyTwitterException(req)
        return search_timeline

    def search_tweet_list_universal(self, q, amount):
        params = {
            "q" : q,
            #'q' : "仕事" + " since:20{}-{}-{}_00:00:00_JST min_faves:1000".format(year,month,day),  #検索文字列
            #'q' : "あけ since:2018-12-31_23:59:59_JST until:2019-01-01_00:00:00_JST",
            'count': amount
        }
        #self.twitter = OAuth1Session(self.KEYS['client_key'],self.KEYS['client_secret'],self.KEYS['access_token'],self.KEYS['access_secret'])
        url = "https://api.twitter.com/1.1/search/universal.json"
        req = self.twitter.get(url, params = params)
        if req.status_code == 200:
            tweet = json.loads(req.text)
            search_timeline = json.loads(req.text)
        else:
            import traceback
            raise MyTwitterException(traceback.print_exc())
        return search_timeline['statuses']
    
    def search_tweet_list_param(self, param, amount):
        params = {
            "q" : q,
            #'q' : "仕事" + " since:20{}-{}-{}_00:00:00_JST min_faves:1000".format(year,month,day),  #検索文字列
            #'q' : "あけ since:2018-12-31_23:59:59_JST until:2019-01-01_00:00:00_JST",
            'count': amount
        }
        url = "https://api.twitter.com/1.1/search/tweets.json"
        req = self.twitter.get(url, params = params)
        if req.status_code == 200:
            tweet = json.loads(req.text)
            search_timeline = json.loads(req.text)
        else:
            import traceback
            raise MyTwitterException(traceback.print_exc())
        return search_timeline['statuses']
    


def search_reply(user_id, tweet_id, count, range):
    # 文字列設定
    user_id += ' exclude:retweets' # RTは除く
    user_id = urllib.parse.quote_plus(user_id)
    # リクエスト
    url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+user_id+"&count="+str(count)
    auth = OAuth1(CK, CKS, AT, ATS)
    response = requests.get(url, auth=auth)
    data = response.json()['statuses']
    # ２回目以降のリクエスト
    cnt = 0
    reply_cnt = 0
    tweets = []
    while True:
        if len(data) == 0:
            break
        cnt += 1
        if cnt > range:
            break
        for tweet in data:
            if tweet['in_reply_to_status_id_str'] == tweet_id: # ツイートIDに一致するものを抽出
                tweets.append(tweet['text'])  # ツイート内容
                reply_cnt += 1
            maxid = int(tweet["id"]) - 1
        url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+user_id+"&count="+str(count)+"&max_id="+str(maxid)
        response = requests.get(url, auth=auth)
        try:
            data = response.json()['statuses']
        except KeyError: # リクエスト回数が上限に達した場合のデータのエラー処理
            print('上限まで検索しました')
            break
    print('検索回数 :', cnt)
    print('リプライ数 :', reply_cnt)
    return tweets
