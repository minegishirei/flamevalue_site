from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt

import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import datetime
import NatureLang
import Sitemap





repo = "twitter_network"
information_page_link = "about.html"
title = "twitter network analytics"

description = "twitter上でアカウント同士の人脈ネットワークを可視化するツールです。"
img = "http://fanstatic.short-tips.info/static/fanstatic/sample.png"

favicon = "https://raw.githubusercontent.com/kawadasatoshi/minegishirei/main/img/beaver.png"


def index(request):
    page_list = Github.seach_page_list(repo)
    htmlname = "all_page.html"
    params = {
        "information_page_link" :information_page_link,
        "title" : title,
        "repo":repo,
        "page_list":page_list,
        "favicon" : favicon,
        "description" : description,
        "img" : img
    }
    return render(request, "fanstatic/dashboard/twitter_network_index.html", params)



@xframe_options_exempt
def page(request, htmlname):
    if htmlname=="about.html":
        return about(request)
    if "reload" in request.GET:
        Github.delete_page(repo, htmlname)
    try:
        upload_network_json(htmlname)
    except Twitter.MyTwitterException:
        return render(request, "fanstatic/dashboard/twitter_network_busy.html", params)
    params = {
        "information_page_link" :information_page_link,
        "acount_name" : htmlname,
        "title" : htmlname + " " +title,
        "repo":repo,
        "favicon" : favicon,
        "description" : description,
        "img" : img
    }
    return render(request, "fanstatic/dashboard/twitter_network.html", params)



def about(request):
    params = {
        "title" : "twitter network analytics Q&A",
        "favicon" : favicon,
        "description" : "twitterアカウントの人脈可視化ツール「twitter network analytics」についてのQ&Aページです。",
        "img" : img
    }
    return render(request, "fanstatic/dashboard/twitter_network_about.html", params)


def upload_network_json(htmlname):
    if not Github.has_already_created(repo, htmlname):
        git_json = create_network_json(htmlname)
        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.upload(repo, htmlname, text)





def create_network_json(root_name):
    root_name = "@" + root_name.replace("@","")
    link_list = []
    acount_list = []
    acount_set = set()
    
    myTwitterAction = Twitter.MyTwitterAction()
    def induction_json(parent_name, depth, node_num):
        if depth < 0:
            return
        tweet_list = myTwitterAction.search_tweet_list(parent_name, amount=100)
        dub_tweet_list, non_dub_tweet_list = get_dub_acount(tweet_list, acount_set)

        for tweet in dub_tweet_list:
            acount_name = "@"+tweet["user"]["screen_name"]
            if acount_name in acount_set:
                pass
            else:
                acount_set.add(acount_name)
                acount_list.append(grep_node_info(tweet))
            link_list.append({
                "target" : acount_name,
                "source" : parent_name,
                "value"  : 1
            })
            induction_json(acount_name, depth-1, int(node_num/2))
        
        for tweet in non_dub_tweet_list[:max(0, node_num -len(dub_tweet_list))]:
            acount_name = "@"+tweet["user"]["screen_name"]
            if acount_name in acount_set:
                pass
            else:
                acount_set.add(acount_name)
                acount_list.append(grep_node_info(tweet))
            link_list.append({
                "target" : acount_name,
                "source" : parent_name,
                "value"  : 1
            })
            induction_json(acount_name, depth-1, int(node_num/2))


    def grep_node_info(tweet):
        base = {
            "name"  : "@" +tweet["user"]["screen_name"],
            "img"   : tweet["user"]["profile_image_url"],
            "text"  : tweet["text"],
            "group" : 1
        }
        return base
    
    def get_dub_acount(tweet_list, acount_set):
        dub_tweet_list = []
        non_dub_tweet_list = []
        for tweet in tweet_list:
            acount_name = "@"+ tweet["user"]["screen_name"]
            if acount_name in acount_set:
                dub_tweet_list.append(tweet)
            else:
                non_dub_tweet_list.append(tweet)
        return dub_tweet_list, non_dub_tweet_list
    
    induction_json(root_name, 1, 50)
    if root_name not in acount_set:
        acount_list.append({
            "name"  : root_name,
            "img"   : "https://cdn.icon-icons.com/icons2/1144/PNG/512/twitterlogo1_80940.png",
            "text"  : "本人",
            "group" : 1
        })
    return {
        "nodes":acount_list,
        "links":link_list
    }


#twitterのJsonをフォーマットしてくれる物が欲しい
