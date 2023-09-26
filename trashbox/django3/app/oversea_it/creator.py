from django.shortcuts import render, redirect
import json
import sys
from datetime import datetime
from datetime import datetime
import time

if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
import markdown
import GoogleTrans

from .mock import test_list
FEATUHER = {
    'access_token' : '968269222525587456-nTufoFnhYpNIY1sLQwB9WYGiDlAIEMM',
    'access_secret' : 'rhoqnAXt3VHz9dnNv8DlyDUd9V1fijfw2Of091UkjVUTV',
    'consumer_key' : 'nAllJpqiUKtnUG4aHrk2G6T9v',
    'consumer_secret' : 'QAY2CnNGt2onuun6QckyYniZeh753q6X4dEXw9mS3pjTecPk9Y'
}

REPO = "oversea_v2_it"

def selector(keyword):
    q = f"lang:en min_faves:300 {keyword}"
    myTwitterAction = Twitter.MyTwitterAction(FEATUHER)
    tweet_list = myTwitterAction.search_tweet_list(q, 100)
    #tweet_list = test_list
    tweetListParser = TweetListParser(tweet_list)
    tweetListParser.diet()
    tweetListParser.date()
    tweetListParser.add_column("title", "t")
    tweetListParser.add_column("supplement", "")
    tweetListParser.add_column("ja_text", "")
    tweetListParser.sort("favorite_count")
    tweetListParser.cutoff(100)
    #tweetListParser.lang_trans()
    new_tweet_list = tweetListParser.get()
    params = {
        "tweet_list" : new_tweet_list
    }
    return params

def editor(request):
    since = request.GET["since"]
    until = request.GET["until"]
    user  = request.GET["user"]
    tweet_id = request.GET["tweet_id"]
    q = f"to:{user} until:{until} since:{since} min_faves:10"
    FEATUHER = {
        'access_token' : '968269222525587456-nTufoFnhYpNIY1sLQwB9WYGiDlAIEMM',
        'access_secret' : 'rhoqnAXt3VHz9dnNv8DlyDUd9V1fijfw2Of091UkjVUTV',
        'consumer_key' : 'nAllJpqiUKtnUG4aHrk2G6T9v',
        'consumer_secret' : 'QAY2CnNGt2onuun6QckyYniZeh753q6X4dEXw9mS3pjTecPk9Y'
    }
    myTwitterAction = Twitter.MyTwitterAction(FEATUHER)
    tweet_list = myTwitterAction.search_tweet_list(q, 100)
    tweetListParser = TweetListParser(tweet_list)
    tweetListParser.diet()
    tweetListParser.date()
    tweetListParser.add_column("title", "t")
    tweetListParser.add_column("supplement", "")
    tweetListParser.sort("date")
    tweetListParser.cutoff(50)
    tweetListParser.lang_trans()
    new_tweet_list = tweetListParser.get()
    if len(new_tweet_list) < 2:
        return {}
    new_tweet_list.insert(0, {
        "title" : user,
        "id" : tweet_id
    })
    json_info = json.dumps(new_tweet_list, ensure_ascii=False, indent=4)
    Github.upload(REPO,  tweet_id+".json", json_info)
    params = {
        "tweet_list" : new_tweet_list
    }
    return params


def save_edit(id, tweet_list):
    Github.delete_page(REPO, id + ".json")
    json_info = json.dumps(tweet_list, ensure_ascii=False, indent=4)
    Github.upload(REPO,  id+".json", json_info)


def update_tweet_list(tweet_list, edit_list):
    tweet_list = tweet_list.copy()
    for tweet_dict in tweet_list:
        for edit_tweet_dict in edit_list:
            if str(tweet_dict["id"]) == str(edit_tweet_dict["id"]):
                tweet_dict.update(edit_tweet_dict)
    return tweet_list

class TweetListParser():
    def __init__(self, tweet_list):
        self.tweet_list = tweet_list
        self.trans_tweet_list = tweet_list
    
    def diet(self):
        #filter_method = ""
        #if filter = "":
        #    filter_method = self.cut
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            new_tweet_list.append(self.cut(tweet))
        self.trans_tweet_list = new_tweet_list
        return self.trans_tweet_list
    
    def cut(self, tweet):
        new_tags = ["id", "text", "retweet_count", "favorite_count", "in_reply_to_status_id", "created_at"]
        new_tweet = {}
        for tag in new_tags:
            new_tweet[tag] = tweet[tag]
        twitterUserParser = TwitterUserParser(tweet["user"])
        new_tweet["user"] = twitterUserParser.cut()
        return new_tweet
    
    def add_column(self, tag, init):
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            tweet[tag] = init
            new_tweet_list.append(tweet)
        self.trans_tweet_list = new_tweet_list
        return self.trans_tweet_list
    
    def filter(self, tag, value):
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            print(tweet["id"])
            print(value)
            if( str(tweet[tag]) == str(value) ):
                new_tweet_list.append(tweet)
        self.trans_tweet_list = new_tweet_list
        return new_tweet_list
    
    def sort(self, tag):
        self.trans_tweet_list = sorted(self.trans_tweet_list, key=lambda x: x[tag])
        self.trans_tweet_list.reverse()
        return self.trans_tweet_list
    
    def cutoff(self, num):
        new_tweet_list = []
        for i, tweet in enumerate(self.trans_tweet_list):
            new_tweet_list.append(tweet)
            if i>= num:
                break
        self.trans_tweet_list = new_tweet_list
        return new_tweet_list
    
    def lang_trans(self):
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            tweet["ja_text"] = GoogleTrans.en_to_ja(tweet["text"])
            print(tweet["ja_text"])
            new_tweet_list.append(tweet)
        self.trans_tweet_list = new_tweet_list
    
    def get(self):
        return self.trans_tweet_list
    
    def date(self):
        new_tweet_list = []
        for tweet in self.trans_tweet_list:
            ts = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            tweet["date"] = ts
            date2 = time.strftime('%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            date2 = '{0:02}'.format(int(date2)+1)
            month = time.strftime('%m', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            year  = time.strftime('%Y', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            tweet["date2"] = year + "-" + month + "-" + date2
            new_tweet_list.append(tweet)
        self.trans_tweet_list = new_tweet_list
    

class TwitterUserParser():
    def __init__(self, user_info):
        self.user_info = user_info
        self.trans_user = {}
    
    def cut(self):
        new_tags = [
            "id", 
            "name", 
            "screen_name", 
            "location", 
            "description", 
            "profile_background_image_url", 
            "profile_image_url",
            "followers_count", 
            "friends_count"
        ]
        for tag in new_tags:
            self.trans_user[tag] = self.user_info[tag]
        return self.trans_user



def main():
    class Request():
        def __init__(self):
            self.GET = {
                "since" : "2022-05-23",
                "until" : "2022-05-24",
                "user"  : "denicmarko",
                "tweet_id"    : "1528678833561509897"
            }
    request = Request()
    params = editor(request)

if __name__ == "__main__":
    main()

