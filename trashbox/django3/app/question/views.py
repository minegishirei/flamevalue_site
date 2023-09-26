from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Yahoo
import MyJson
import NatureLang
import datetime
# Create your views here.


all_category = {
    "mental"    : "https://chiebukuro.yahoo.co.jp/category/2078297858/question/list?page={}",
    "it"        : "https://chiebukuro.yahoo.co.jp/category/2078297616/question/list?page={}",
    "code"      : "https://chiebukuro.yahoo.co.jp/category/2078297622/question/list?page={}",
    "net"       : "https://chiebukuro.yahoo.co.jp/category/2078297628/question/list?page={}"
}


####################




class AddContentManager():
    def __init__(self):
        """
        ユーザーに後悔するページを登録するjsonファイル
        """
        self.myJson = MyJson.MyLocalJson("/app/question/addContent.json")
        
    def addContent(self, category, yahoo_id):
        yahooQuestionPage = Yahoo.YahooQuestionPage("https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q" + yahoo_id)
        content = yahooQuestionPage.collect()
        #get data
        new_dict = {
            "yahoo_id"  : yahoo_id,
            "content"   : content
        }
        #add to json_file
        before_dict = self.myJson.read()
        before_dict[category]["page_list"].append(new_dict)
        self.myJson.write(before_dict)
        
    def loadContent(self, category, yahoo_id):
        return_json = self.myJson.read()
        for page_dict in return_json[category]["page_list"]:
            if page_dict["yahoo_id"] == yahoo_id:
                return page_dict
    
    def loadCategory(self, category):
        return self.myJson.read()[category]
    
    def preProcessing(self):
        pass
    
    def update_JsonTable(self):
        pass
####################



addContentManager = AddContentManager()

global_params = {
"site_name": "こんな質問を見つけた",
"all_category" : all_category
}


def index(request):
    global global_params
    params = global_params.copy()
    params.update({
        "title" : "こんな質問を見つけた"
    })
    return render(request,"question/index.html",params)

def robots(request):
    return render(request, f"robots.txt")


def sitemap(request):
    the_json = addContentManager.myJson.jsondict
    page_list = []
    for category_name, category_dict in the_json.items():
        for page_dict in category_dict["page_list"]:
            yahoo_id = page_dict["yahoo_id"]
            url = f"http://question.short-tips.info/{category_name}/{yahoo_id}"
            page_list.append(url)
    
    dt_now = datetime.datetime.now()
    params = {}
    params.update({
        "page_list" : page_list,
        "last_mod"  :f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    })
    return render(request, "question/sitemap.xml", params)



def category_list(request, category):
    global global_params
    params = global_params.copy()
    params.update({
        "title" : "こんな質問を見つけた | " + category
    })
    if request.GET.get("edit"):
        page_info_list = Yahoo.main(all_category[category])
        params.update({
            "category" : category,
            "page_info_list" : page_info_list
        })
        return render(request,"question/category_list_edit.html",params)
    elif request.GET.get("alladd"):
        page_info_list = Yahoo.main(all_category[category])
        for page_dict in page_info_list:
            yahoo_id = page_dict["id"]
            addContentManager.addContent(category, yahoo_id)
        params.update({
            "category" : category,
            "page_info_list" : page_info_list
        })
        return render(request,"question/category_list_edit.html",params)
    else:
        category_dict = addContentManager.loadCategory(category)
        params.update({
            "category" : category,
            "page_info_list" : category_dict["page_list"]
        })
        return render(request,"question/category_list.html",params)
    


def page(request, category, yahoo_id):
    global global_params
    if request.GET.get("add"):
        addContentManager.addContent(category, yahoo_id)
    page_dict = addContentManager.loadContent(category, yahoo_id)
    params = global_params.copy()
    title = page_dict["content"]["title"]
    params.update({
        "page_dict" : page_dict,
        "title" : title,
        "description" : title,
        "api_responce" : list(NatureLang.get_wordlist(title).keys())[:3]
    })
    return render(request,"question/page.html",params)





