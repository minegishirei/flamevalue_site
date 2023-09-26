# Create your views here.
from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
import GoogleTrans


all_ranking_static = "/static/engineer/data/"
all_ranking_folder = "/app/static/engineer/data/"


favicon = "https://raw.githubusercontent.com/kawadasatoshi/minegishirei/main/img/beaver.png"
img =     "http://techtweetrank.short-tips.info/static/engineer/img/twitter_profile_image.png"
site_name = "ITトレンド"
description = "厳選されたIT業界の最新の情報をお届けします。最新のITトレンド情報を入手しましょう。"

content_type_dict = {
    "page" : {
        "content_type" : "page",
        "title" :  site_name,
        "description" : description,
        "favicon" : favicon,
        "img": img,
        "repo":"engineer_rank",
        "tag_list" : Github.seach_page_list("engineer_rank"),
        "query" : '"{}"' + " lang:ja min_faves:100"
    },"overseas":{
        "content_type" : "overseas",
        "title" : site_name+" 海外版",
        "description" : description,
        "favicon" : favicon,
        "img": img,
        "repo":"overseas",
        "tag_list" : Github.seach_page_list("overseas"),
        "query" : '"{}"' + " lang:en min_faves:100"
    },"legends" : {
        "content_type" : "legends",
        "title" : site_name + " 殿堂入り",
        "description" : description,
        "favicon" : favicon,
        "img": img,
        "repo":"legends",
        "tag_list" : Github.seach_page_list("legends"),
        "query" : '"{}"' + " since:2009-1-1 until:2021-4-1"
    }
}


routine_time = 0
def routine_update():
    global routine_time
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d')
    if routine_time != now:
        routine_time = now
        content_type_dict["page"].update({
            "tag_list" : Github.seach_page_list("engineer_rank"),
        })
        content_type_dict["overseas"].update({
            "tag_list" : Github.seach_page_list("overseas"),
        })
        content_type_dict["legends"].update({
            "tag_list" : Github.seach_page_list("legends"),
        })
    
routine_update()


def allforall_ranking():
    repo = "content_type"



def sitemap(request):
    return render(request,f"ranking/sitemap.xml")

def robots(request):
    return render(request, f"robots.txt")

def about(request):
    htmlname = "about.html"
    params = content_type_dict["page"].copy()
    params.update({
        "htmlname" : htmlname
    })
    return render(request,f"ranking/{htmlname}",params)

def index(request):
    return redirect("/about.html")

def content_index(request, content_type):
    dt_now = datetime.datetime.now()
    all_ranking_filename = content_type + dt_now.strftime('%Y%m%d%H') +".json"
    params = (content_type_dict[content_type]).copy()
    repo = params["repo"]
    tweet_list = []
    if not Github.has_already_created("content_type", all_ranking_filename):
        for tag in params["tag_list"]:
            json_string = Github.load(repo, tag)
            if len(json_string) < 10:
                continue
            tweet_list = json.loads(json_string)["tweet_list"]
            tweet_list = sort_tweet_list(tweet_list)
            tweet_list = tweet_list[:50]
        text = json.dumps(tweet_list, ensure_ascii=False, indent=4)
        Github.upload("content_type", all_ranking_filename, text )
    params.update({
        "all_ranking_file" : all_ranking_filename,
        "tweet_list":tweet_list
    })
    return render(request,f"ranking/index.html",params)


# Create your views here.
def page(request,content_type, htmlname, pagetype):
    params = content_type_dict[content_type].copy()
    repo = params["repo"]
    params.update({
        "htmlname" : htmlname
    })
    if Github.has_already_created(repo, htmlname):
        return render(request,f"ranking/{pagetype}",params)
    else:
        #処理は次のページに任せて、まずは飛ぶ
        return render(request,f"ranking/data_loading.html",params)


def data_loading(request,content_type, htmlname):
    params = content_type_dict[content_type].copy()
    repo = params["repo"]
    query = params["query"].format(htmlname)
    params.update({
        "htmlname" : htmlname
    })
    if not Github.has_already_created(repo, htmlname):
        tweet_list = []
        myTwitterAction = Twitter.MyTwitterAction()
        if content_type == "legends":
            tweet_list = myTwitterAction.search_tweet_list_universal(
            query,
            amount=50)
        elif content_type == "overseas":
            tweet_list = myTwitterAction.search_tweet_list(
                query,
                amount=50)
            try:
                tweet_list = translate_tweet_list(tweet_list)
            except:
                pass
        else:
            tweet_list = myTwitterAction.search_tweet_list(
                query,
                amount=50)
            
        git_json = {}
        git_json.update({
            "tweet_list" : tweet_list
        })
        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.upload(repo, htmlname, text)
    return render(request,f"ranking/ranking.html",params)



def sort_tweet_list(tweet_list):
    tweet_list = sorted(tweet_list, key=lambda x:x["retweet_count"], reverse=True)
    return tweet_list


def translate_tweet_list(tweet_list):
    new_tweet_list = []
    for tweet in tweet_list:
        try:
            text = str(tweet["text"])
            new_text = GoogleTrans.en_to_ja(text)
            tweet.update({
                "text" : new_text
            })
        except:
            pass
        finally:
            new_tweet_list.append(tweet)
    return new_tweet_list



TWEET_LIST = "tweet_list"
TWEET_ID = ""
def edit_page(request, tweet_id):
    global TWEET_ID
    params = {}

    #新規作成
    if tweet_id != TWEET_ID:
        TWEET_ID = tweet_id
        tweet_list = load_tweet_list(tweet_id)
        tweet_list = translate_tweet_list(tweet_list)
        tweet_list = editable_tweet_list(tweet_list)
        tweet_list.session["tweet_list"] = tweet_list
    
    #更新(tweet_list)
    for tweet in tweet_list:
        getSessionValue()

    #buildが押されたのか?

    
    return render(request, "", params)

    

    
def editable_tweet_list(tweet_list):
    new_tweet_list = []
    for tweet in tweet_list:
        tweet.update({
            "title" : "",
            "comment" : "",
            "does_use" : "False"
        })
        new_tweet_list.append()
    return new_tweet_list


def load_tweet_list(tweet_id):
    pass

def getSessionValue(request, key):
    ans = request.POST.get(key)
    if ans is None:
        return ""
    return ans
