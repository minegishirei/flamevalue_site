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


favicon = "https://raw.githubusercontent.com/kawadasatoshi/minegishirei/main/img/beaver.png"
img =     "https://gaijinpot.scdn3.secure.raxcdn.com/app/uploads/sites/4/2019/10/How-much-does-a-foreign-engineer-make-in-Japan-in-2019.jpg"#"/static/techblog/img/feature.png"#"http://techtweetrank.short-tips.info/static/engineer/img/twitter_profile_image.png"
site_explain = "社内SEの業務内容を可能な限りリアルに記しました。これから目指す人も、そうでないエンジニアも楽しめるように書きます！"
site_name = "社内SE雑記ブログ"



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


def genPageDict(repo):
    max_pages = 10000
    category_list = Github.seach_page_list(repo, "/")
    page_dict = {}
    for category in category_list[:max_pages]:
        try:
            category_dict = {}
            for htmlname in Github.seach_page_list(repo, category)[:max_pages]:
                mk = Github.load(repo, category + "/" +htmlname)
                params =  grep_param(mk, ["title", "description", "img", "redirect"])
                if "escape" in params:
                    continue
                params.update({
                    "category" : category,
                    "htmlname" : htmlname
                })
                category_dict[htmlname] = params
            page_dict[category] = category_dict
        except:
            pass
    return page_dict


repo_page_dict = json.loads( Github.load("meta", "/blogs/hosts.json") )
for key, value in repo_page_dict.items():
    repo_page_dict[key] = genPageDict(key)


def sitemap(request):
    repo = request.get_host().split(".")[0]
    pop_page_list = []
    for category_key in repo_page_dict[repo].keys():
        category_dict = repo_page_dict[repo][category_key]
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
        "pop_page_list" : pop_page_list_copy,
        "host_name" : repo
    }
    return render(request,f"sitemap.xml", params)


def index(request):
    global repo_page_dict
    repo = request.get_host().split(".")[0]
    if request.GET.get("reload"):
        repo_page_dict[repo] = genPageDict(repo)
    page_list = []
    if repo == "localhost":
        return redirect("https://techblog.localhost")
    if repo == "short-tips":
        return redirect("https://techblog.short-tips.info")
    for category, category_list in repo_page_dict[repo].items():
        for page in category_list.values():
            page_list.append(page)
    params = {
        "page_list" : page_list,
        "title" : repo + "ブログ",
        "description" : "エンジニア/リクルーター/ブロガー 人材関連企業の社内SEの実態に基づき記述しました。",
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name,
        "category_list" : repo_page_dict[repo]
    }
    return render(request,f"blog_ver2/techblog_ver2/page/index.html",params)


def about(request):
    params = {
        "title" : site_name,
        "description" : site_explain,
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name
    }
    return render(request,f"blog_ver2/techblog_ver2/page/about.html",params)


def page(request, category, htmlname):
    repo = request.get_host().split(".")[0]
    try:
        mk = Github.load(repo, category + "/" +htmlname)
    except:
        return redirect("/" + category + "/")
    tableIndex = TableIndex(mk)
    mk = tableIndex.rebuild_mk()
    params = {
        "mk" : mk,
        "site_name" : site_name,
        "category" : category,
        "favicon" : favicon,
        "htmlname" : htmlname,
        "category_list" : repo_page_dict[repo]
    }
    params.update(grep_param(mk, ["title", "description", "img", "category_script", "redirect"]))
    if "redirect" in params:
        return redirect(params["redirect"])
    if category=="slides":
        return render(request, "blog/non_base.html",params)
    relation_list = []
    if "category_script" in params:
        category_script = params["category_script"]
        category_dict = repo_page_dict[repo][category]
        for page_name, category_dict in category_dict.items():
            if eval(category_script):
                relation_list.append(category_dict)
    params.update({
        "relation_list" : relation_list,
        "index_table" : tableIndex.index_table,
        "favicon" : favicon,
        "is_bite_page" : False
    })
    if request.GET.get("bite_title"):
        params = bite_page(request, params)
        params.update({"is_bite_page": True})
    if request.GET.get("raw"):
        return render(request,f"blog/raw.html", params)
    return render(request,f"blog_ver2/techblog_ver2/page/page.html", params)


def bite_page(request, params):
    bite_title = request.GET.get("bite_title")
    def grep_bite_page(bite_title, context):
        bite_context = ""
        paragraph_count = 0
        is_in_paragraph = False
        for row in context.split('\n'):
            if bite_title in row:
                paragraph_count = row.count("#")
                is_in_paragraph = True
                bite_context = ( bite_context + row + '\n') 
                continue
            if is_in_paragraph:
                if ("#"*paragraph_count in row) and ("#"*(paragraph_count+1) not in row):
                    break
                bite_context = ( bite_context + row + '\n')
        return bite_context
    params.update({
        "mk" : grep_bite_page(bite_title, params["mk"]),
        "title" : bite_title
    })
    return params


def category_page(request, category_name):
    repo = request.get_host().split(".")[0]
    page_list=[]
    try:
        category_dict = repo_page_dict[repo][category_name]
    except:
        return redirect("/")
    for category in category_dict.values():
        page_list.append(category)
    params = {
        "page_list" : page_list,
        "title" : repo,
        "description" : "",
        "favicon" : favicon,
        "img": img,
        "site_name" : site_name,
        "category" : category_name,
        "category_list" : repo_page_dict[repo]
    }
    return render(request,f"blog_ver2/techblog_ver2/page/category.html", params)


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
                self.index_table[h2_count] = row.replace("#", "")
                new_mk += (f'<div id="{h2_count}">' + "\n")
                new_mk += ("</div>\n\n")
                new_mk += (row + "\n")
                new_mk += "\n<hr>\n"
            else:
                new_mk += (row + "\n")
        return new_mk
