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


repo = "techblog"


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


def genPageDict():
    category_list = [
        "docker",
        "powershell", 
        "career",
        "python", 
        "kotlin",
        "sql",
        "inhouse_se", 
        #"design", 
        #"developper", 
        #"os", 
        #"programming",
        #"deeplearning",
        "html_css",
        "javascript",
        #"management",
        "vb6",
        #"ctf",
        "else"]
    page_dict = {}
    for category in category_list:
        category_dict = {}
        for htmlname in Github.seach_page_list(repo, category):
            mk = Github.load(repo, category + "/" +htmlname)
            params =  grep_param(mk, ["title", "description", "img"])
            if "escape" in params:
                continue
            params.update({
                "category" : category,
                "htmlname" : htmlname
            })
            category_dict[htmlname] = params
        page_dict[category] = category_dict
    return page_dict

clock = 0
page_dict = genPageDict()

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
    pop_page_list = []
    for category_key in page_dict.keys():
        category_dict = page_dict[category_key]
        for html_key in category_dict.keys():
            pop_page_list.append({
                "category" : category_key,
                "htmlname" : html_key
            })
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d%H')
    pop_page_list_copy = pop_page_list.copy()
    for page in pop_page_list_copy:
        page["lastmod"] = f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    params = {
        "pop_page_list" : pop_page_list_copy
    }
    return render(request,f"blog/techblog/page/sitemap.xml", params)


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
    return render(request,f"blog/techblog_ver2/page/index.html",params)


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
def page(request, category, htmlname):
    mk = Github.load(repo, category + "/" +htmlname)
    tableIndex = TableIndex(mk)
    mk = tableIndex.rebuild_mk()
    md = markdown.Markdown()
    htmltext = md.convert(mk)
    params = {
        "mk" : mk,
        "htmltext" : htmltext,
        "site_name" : site_name,
        "category" : category,
        "favicon" : favicon,
        "htmlname" : htmlname
    }
    params.update(grep_param(mk, ["title", "description", "img", "category_script", "redirect"]))
    if "redirect" in params:
        return redirect(params["redirect"])
    if category=="slides":
        return render(request, "blog/non_base.html",params)
    
    relation_list = []
    if "category_script" in params:
        category_script = params["category_script"]
        category_dict = page_dict[category]
        for page_name, category_dict in category_dict.items():
            if eval(category_script):
                relation_list.append(category_dict)
    
    params.update({
        "index_table" : tableIndex.index_table
    })

    params.update({
        "relation_list" : relation_list
    })
    if request.GET.get("raw"):
        return render(request,f"blog/raw.html", params)
    return render(request,f"blog/techblog_ver2/page/page.html", params)


def category_page(request, category_name):
    page_list=[]
    category_dict = page_dict[category_name]
    for category in category_dict.values():
        page_list.append(category)
    
    title_dict = {
        "docker" : "Docker学習サイト",
        "kotlin" : "Kotlin学習サイト",
        "inhouse_se" : "社内SE雑記ブログ",
        "python" : "python学習サイト",
        "powershell": "powershell学習サイト",
        "deeplearning" : "機械学習入門サイト",
        "else" : "社内SE雑記ブログ その他記事",
        "sql" : "SQL学習サイト",
        "career" : "キャリアメモ",
        "javascript" : "Javascriptメモ",
        "html_css" : "html/CSSメモ",
        "management" : "マネジメントメモ",
        "vb6" : "vb6学習サイト",
        "ctf" : "CTFチャレンジサイト"
    }
    description_dict = {
        "docker" : "dockerの環境構築からdockerのhelloworld,dockerでサーバーを立てる方法までを解説します。",
        "inhouse_se" : site_explain,
        "kotlin" : "kotlinの環境構築から基本的な文法をまとめました。",
        "python" : "pythonの中級者向けの備忘録サイトです。機械学習やオートメーションを解説します。",
        "powershell": "windows10の自動化の鍵となるパワーシェルについて変数の扱いからfor文までまとめました。",
        "deeplearning" : "機械学習入門サイト",
        "else" : site_explain,
        "career" : "キャリアに関するメモです。転職に関する内容や転職ドラフトでの記載内容についての備忘録です。",
        "sql" : "SQLの基本的な文法やOracleのブロンズの資格試験対策、実際のコードのサンプル集など。",
        "javascript" : "Javascriptに関するメモを備忘録として収録しております。D3.jsやBackbone.js,Reactなどについて。",
        "html_css" : "html/CSSメモ",
        "management" : "マネジメントメモ",
        "vb6" : "vb6学習サイト",
        "ctf" : "CTFチャレンジサイト"
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
    
    return render(request,f"blog/techblog_ver2/page/category.html", params)




class TableIndex():
    def __init__(self, mk):
        self.mk = mk
        self.index_table = {}

    def rebuild_mk(self):
        in_pre_flag = False
        h2_count = 0
        new_mk = ""
        for row in self.mk.split('\n'):
            if "<pre>" in row:
                in_pre_flag = True
            if "</pre>" in row:
                in_pre_flag = False
            
            if (not in_pre_flag) and row.startswith("##"):
                h2_count += 1
                self.index_table[h2_count] = row.replace("##", "")
                new_mk += (f'<div id="{h2_count}">' + "\n")
                new_mk += ("</div>\n")
                new_mk += (row + "\n")
                new_mk += "<hr>\n"
            else:
                new_mk += (row + "\n")
        return new_mk

    
