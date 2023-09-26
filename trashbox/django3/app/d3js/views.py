# Create your views here.
from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Sitemap
import Statichub
import datetime
import markdown


all_ranking_static = "/static/engineer/data/"
all_ranking_folder = "/app/static/engineer/data/"



favicon = "https://raw.githubusercontent.com/kawadasatoshi/minegishirei/main/img/beaver.png"
img =     "https://gaijinpot.scdn3.secure.raxcdn.com/app/uploads/sites/4/2019/10/How-much-does-a-foreign-engineer-make-in-Japan-in-2019.jpg"#"/static/techblog/img/feature.png"#"http://techtweetrank.short-tips.info/static/engineer/img/twitter_profile_image.png"
site_explain = "社内SEの業務内容を可能な限りリアルに記しました。これから目指す人も、そうでないエンジニアも楽しめるように書きます！"
site_name = "社内SE雑記ブログ"


repo = "d3js_ja_documents"


def robots(request):
    return render(request, f"robots.txt")

def grep_param(mk, taglist):
    params = {}
    for tag in taglist:
        for line in mk.split("\n"):
            if line.startswith(tag+":"):
                try:
                    params.update({
                        tag : line.replace(tag + ":", "" )
                    })
                except:
                    pass
    return params

"""
def genPageDict():
    category_list = [
        "python", 
        "inhouse_se", 
        "deeplearning",
        "powershell", 
        "else"]
    page_dict = {}
    for category in category_list:
        category_dict = {}
        for htmlname in Github.seach_page_list(repo, category):
            mk = Github.load(repo, category + "/" +htmlname)
            params =  grep_param(mk, ["title", "description", "img"])
            params.update({
                "category" : category,
                "htmlname" : htmlname
            })
            category_dict[htmlname] = params

        page_dict[category] = category_dict
    return page_dict
"""

clock = 0
#page_dict = genPageDict()

def checkandrenew():
    global clock
    global page_dict
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d%H')
    if clock != now:
        clock = now
        page_dict = genPageDict()
        return True
    return False


def sitemap(request):
    page_list = []
    page_list.append("http://d3js.short-tips.info/index.html")
    for htmlname in Github.seach_page_list(repo):
        page_list.append(f"http://d3js.short-tips.info/{htmlname}")
    return Sitemap.sitemap(request, page_list)


def index(request):
    global page_dict
    if request.GET.get("reload"):
        page_dict = genPageDict()
    page_list = []
    for category, category_list in page_dict.items():
        for page in category_list.values():
            page_list.append(page)
    params = {
        "page_list" : page_list,
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name
    }
    return render(request,f"blog/techblog/page/index.html",params)


def about(request):
    params = {
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name
    }
    return render(request,f"blog/techblog/page/about.html",params)


# Create your views here.
def page(request, htmlname):
    plain_html = Github.load(repo, htmlname)
    #md = markdown.Markdown()
    #htmltext = md.convert(mk)
    params = {
        "main_contents" : plain_html
    }
    #/Users/minegishirei/myworking/docker/django3/app/d3js/templates/d3js/base.html
    return render(request,f"d3js/base.html", params)


def category_page(request, category_name):
    page_list=[]
    category_dict = page_dict[category_name]
    for category in category_dict.values():
        page_list.append(category)
    
    title_dict = {
        "inhouse_se" : "社内SE雑記ブログ",
        "python" : "python学習サイト",
        "powershell": "powershell学習サイト",
        "deeplearning" : "機械学習入門サイト",
        "else" : "社内SE雑記ブログ その他記事"
    }
    params = {
        "page_list" : page_list,
        "title" : title_dict[category_name],
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name,
        "category" : category_name
    }
    
    return render(request,f"blog/techblog/page/category.html", params)


