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


favicon = "/static/techblog/img/feature.png"
img =     "https://gaijinpot.scdn3.secure.raxcdn.com/app/uploads/sites/4/2019/10/How-much-does-a-foreign-engineer-make-in-Japan-in-2019.jpg"#"/static/techblog/img/feature.png"#"http://techtweetrank.short-tips.info/static/engineer/img/twitter_profile_image.png"
site_explain = "社内SEの業務内容を可能な限りリアルに記しました。これから目指す人も、そうでないエンジニアも楽しめるように書きます！"
site_name = "心理学ガチまとめ"


repo = "psy"


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


category_list = [
    "baum",
    "color",
    "copywriting",
    "design",
    "face",
    "furniture",
    "material",
    "methods_features",
    "methods_union",
    "phrase",
    "soundsymbol",
    "the_war"
]
category_title_dict = {
    "baum" : "バウムテスト総まとめブログ",
    "color" : "色にまつわる心理学まとめ",
    "copywriting" : "コピーライティング実践編",
    "design" : "デザインまとめブログ",
    "face" : "顔の心理学",
    "furniture" : "家具にまつわる心理学まとめ",
    "material" : "家具にまつわる心理学まとめ",
    "methods_union" : "人を動かす心理学",
    "phrase" : "人を動かせる言葉",
    "soundsymbol" :"音象徴について",
    "the_war" : "戦争の心理学"
}
category_description_dict = {
    "baum" : "バウムテスト総まとめブログ",
    "color" : "色にまつわる心理学まとめ",
    "copywriting" : "コピーライティング実践編",
    "design" : "デザインまとめブログ",
    "face" : "顔の心理学",
    "furniture" : "家具にまつわる心理学まとめ",
    "material" : "家具にまつわる心理学まとめ",
    "methods_union" : "人を動かす心理学",
    "phrase" : "人を動かせる言葉",
    "soundsymbol" :"音象徴について",
    "the_war" : "戦争の心理学"
}

def genPageDict():
    global category_list
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
    return render(request,f"blog/techblog_ver3/sitemap.xml", params)


def index(request):
    global page_dict
    if request.GET.get("reload"):
        page_dict = genPageDict()
    page_list = []
    for category, category_list2 in page_dict.items():
        for page in category_list2.values():
            page_list.append(page)
    params = {
        "page_list" : page_list,
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name,
        "category_list" : category_list,
    }
    return render(request,f"blog/techblog_ver3/page/index.html",params)


def about(request):
    params = {
        "category_"
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
        "htmlname" : htmlname,
        "category_list" : category_list,
    }
    params.update(grep_param(mk, ["title", "description", "img", "category_script"]))
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
    return render(request,f"blog/techblog_ver3/page/page.html", params)


def category_page(request, category_name):
    page_list=[]
    category_dict = page_dict[category_name]
    for category in category_dict.values():
        page_list.append(category)
    
    params = {
        "category_list" : category_list,
        "page_list" : page_list,
        "title" : category_title_dict[category_name],
        "description" : category_description_dict[category_name],
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name,
        "category" : category_name
    }
    
    return render(request,f"blog/techblog_ver3/page/category.html", params)




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

    
