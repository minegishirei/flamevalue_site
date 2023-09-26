from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import datetime
import NatureLang
import Sitemap

dt_now = datetime.datetime.now()

repo = "twitter_json"
filename = "access_ranking" + dt_now.strftime('%Y%m%d')

favicon = "https://raw.githubusercontent.com/kawadasatoshi/minegishirei/main/img/beaver.png"
img =     "http://fanstatic.short-tips.info/static/dashboard/img2/thumbnail2.png"
site_explain = "あなたのアカウントを可能な限り分析します"
ranking_list = []


def get_pagetype_title(key):
    pagetype_title_dict = {
        "dashboard.html" : " | twitterアカウント分析サイト",
        "charts.html" : " | twitterアカウント分析サイト",
        "word_cloud.html" : "が一目で分かる！"
    }
    if key in pagetype_title_dict:
        return pagetype_title_dict[key]
    return " | twitterアカウント分析サイト"


def sitemap(request):
    acount_list = Github.seach_page_list(repo)
    page_list = []
    url_template_list = [
        "https://fanstatic.short-tips.info/index.html?screen_name={}",
        #"http://fanstatic.short-tips.info/page/{}/dashboard.html",
        #"http://fanstatic.short-tips.info/page/{}/charts.html",
        "https://fanstatic.short-tips.info/page/{}/word_cloud.html"
        #"http://fanstatic.short-tips.info/page/{}/tables.html"
    ]
    for acount in acount_list:
        for url_base in url_template_list:
            page_list.append(url_base.format(acount))
    
    acount_list = Github.seach_page_list("twitter_network")
    url_template_list = [
        "https://fanstatic.short-tips.info/twitter_network/{}"
    ]
    for acount in acount_list:
        for url_base in url_template_list:
            page_list.append(url_base.format(acount))
    page_list.append("https://fanstatic.short-tips.info/twitter_network/")
    page_list.append("https://fanstatic.short-tips.info/twitter_network/about.html")
    return Sitemap.sitemap(request, page_list)
    #return render(request,f"fanstatic/sitemap.xml")


def index(request):
    htmlname = "index2.html"
    screen_name = request.GET.get("screen_name")
    params = {
        "title" : screen_name + "で検索したあなたへ",
        "description" : "あなたのtwitterアカウントのアカウントをフォロワー数や年齢層からツイートコンテンツの内容までの観点で分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    params.update({
        "screen_name" : screen_name,
        "screen_name_raw" : screen_name.replace("@", "").replace(" ", "") ,
        "ranking_list":ranking_list
    })
    return render(request,f"AdminLTE-master/{htmlname}",params)



def pop_page(request):
    result = seach(request)
    if result:
        return result
    htmlname = "pop_page.html"
    params = {
        "title" : "人気ランキング | twitterアカウント分析サイト",
        "description" : "あなたのtwitterアカウントのアカウントをフォロワー数や年齢層からツイートコンテンツの内容までの観点で分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    params.update({
        "ranking_list":ranking_list
    })
    return render(request,f"fanstatic/dashboard/top/{htmlname}",params)



def all_page(request):
    result = seach(request)
    if result:
        return result
    page_list = Github.seach_page_list(repo)
    htmlname = "all_page.html"
    params = {
        "title" : "twitterアカウント分析サイト",
        "description" : "あなたのtwitterアカウントのアカウントをフォロワー数や年齢層からツイートコンテンツの内容までの観点で分析します。",
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    params.update({
        "ranking_list":page_list
    })
    return render(request,f"fanstatic/dashboard/top/{htmlname}",params)


# Create your views here.
def page(request, htmlname, pagetype):
    explain = ""
    metadata = {}
    for content in ranking_list:
        if content["name"] == htmlname:
            metadata = content
            explain = metadata["description"]
    if explain == "":
        explain = site_explain
    result = seach(request)
    if result:
        return result
    params = {
        "title" : htmlname + get_pagetype_title(pagetype),
        "description" : explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
        "explain": explain
    }
    if Github.has_already_created(repo, htmlname):
        return render(request,f"fanstatic/dashboard/{pagetype}",params)
    else:
        #処理は次のページに任せて、まずは飛ぶ
        return render(request,f"fanstatic/dashboard/data_loading.html",params)

def creation_page(request, htmlname, pagetype):
    result = seach(request)
    if result:
        return result
    params = {
        "title" : htmlname + " | twitterアカウント分析",
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }


def data_loading(request, htmlname):
    result = seach(request)
    if result:
        return result
    params = {
        "title" : "twitterアカウント分析サイト",
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "repo":repo,
        "htmlname" : htmlname,
    }
    if not Github.has_already_created(repo, htmlname):
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list(htmlname, amount=50)
        
        git_json = {}
        git_json.update({
            "tweet_list" : tweet_list
        })

        git_json.update({
            "wordcloud" : genWordList(tweet_list)
        })

        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.upload("twitter_json", htmlname, text)
    return render(request,f"fanstatic/dashboard/dashboard.html",params)


def seach(request):
    if "request_word" in request.GET:
        request_word = request.GET["request_word"]
        return redirect(f"/page/{request_word}/dashboard.html")
    return False

def robots( request):
    return render(request, 'meta/robots.txt')


def genWordList(tweet_list):
    all_text = ""
    for tweet in tweet_list:
        text = tweet["text"]
        all_text += text
    
    def yield_text(all_text):
        split_text = list(all_text.split("。"))
        return_text = ""
        for text in split_text:
            tmp_text = return_text
            return_text += text
            if len(return_text) > 400:
                yield tmp_text
                return_text = ""
                tmp_text = ""

    count = 0
    return_list = []
    for text in yield_text(all_text):
        if count> 10:
            break
        count+=1
        try:
            return_list.extend( NatureLang.get_wordlist(text) )
        except:
            pass
    return return_list




