from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
import markdown
# Create your views here.

from .creator import selector, editor


favicon = "/static/oversea_it/img/favicon.png"
img =     "http://techtweetrank.short-tips.info/static/oversea_it/img/header.png"
site_explain = "海外のITニュースをお届けします。"
site_name = "海外エンジニアまとめ"


param_tag_list = [
    "title", 
    "description", 
    "sub_title", 
    "img"
    ]


base_template = "oversea_it/base/page.html"

repo = "oversea_it"

category_list = [
    "os",
    "programming",
    "design",
    "developper"
]


def grep_param(mk, taglist):
    params = {}
    for tag in taglist:
        for line in mk.split("\n"):
            if line.startswith(tag+":"):
                params.update({
                    tag : line.replace(tag + ":", "" )
                })
    return params


page_dict = {}
def genPageDict():
    global page_dict
    for category in category_list:
        category_dict = {}
        for htmlname in Github.seach_page_list(repo, category)[:3]:
            mk = Github.load(repo, category + "/" +htmlname)
            md = markdown.Markdown()
            htmltext = md.convert(mk)
            params =  grep_param(mk, param_tag_list)
            params.update({
                "category" : category,
                "htmlname" : htmlname,
                "htmltext" : htmltext
            })
            category_dict[htmlname] = params
        page_dict[category] = category_dict
    return page_dict
#page_dict = genPageDict()



def getMetaInfo():
    global meta_info
    json_string = Github.load(repo, "pop_page_list.json")
    pop_page_json = json.loads(json_string)
    pop_page_list = []
    for pop_page in pop_page_json:
        pop_path = pop_page.split("/")
        category = pop_path[0]
        htmlname = pop_path[1]
        pop_page_info = page_dict[category][htmlname]
        pop_page_list.append(pop_page_info)
    return pop_page_list
#pop_page_list = getMetaInfo()
pop_page_list = []

def index(request):
    global page_dict
    global pop_page_list
    if request.GET.get("selector"):
        params = selector(request)
        return render(request,"oversea_it/base/index.html")
    if request.GET.get("editor"):
        params = editor(request)
        return render(request,"oversea_it/base/index.html", params)
    if request.GET.get("reload"):
        page_dict = genPageDict()
        pop_page_list = getMetaInfo()
        
    params = {
        "category_list" : category_list,
        "page_dict" : page_dict,
        "pop_page_list" : pop_page_list,
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name
    }
    return render(request,"oversea_it/base/index.html",params)



def robots(request):
    return render(request, f"robots.txt")

def about():
    pass

def category_page(request, category):
    pass

# Create your views here.
def page(request, category, htmlname):
    category_dict = page_dict[category]
    params = (category_dict[htmlname]).copy()
    params.update({
        "category_list" : category_list,
        "pop_page_list" : pop_page_list,
        "favicon" : favicon
    })

    return render(request,base_template, params)





def reload(request):
    pop_page_list = getMetaInfo()
    page_dict = genPageDict()
    return redirect("/index.html")






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
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d%H')
    pop_page_list_copy = pop_page_list.copy()
    for page in pop_page_list_copy:
        page["lastmod"] = f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    params = {
        "pop_page_list" : pop_page_list_copy
    }
    return render(request,f"oversea_it/sitemap.xml", params)



def about(request):
    params = {
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name
    }
    return render(request,f"oversea_it/sitemap.xml",params)




