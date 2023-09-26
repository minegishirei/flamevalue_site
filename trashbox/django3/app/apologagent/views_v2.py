from django.shortcuts import render
from .sentense_class import InputText, Choice
from django.views.decorators.csrf import csrf_exempt

import json
import sys

if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import UniqueAPI

repo = "apologagent"


pageInfoDict = {
    "oko.html" :{
        "params" :  {
            "title" : "反省書自動作成システム",
            "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
            "favicon" : "/static/チャット.png",
            "img": "http://apologagent.short-tips.info/static/thumbnail.png",
            "sample" : """この度は（一時間以上も遅刻）してしまい、大変申し訳ございませんでした。
皆様に多大なご迷惑をおかけしたことを申し上げます。
直接の原因は（アラームを設定し忘れた）ことが原因です。
今後はこのようなことが２度と起きぬよう 、再発防止に努めます。""",
            "volume" : 2
        },"transition" : [{
                "process":0,
                "name": "input1",
                "title": "結論",
                "supp":"あなたは何をやらかしました？",
                "preface":"この度は",
                "example":"定例会議に15分以上も遅刻してしまい",
                "afterword":"、申し訳ございませんでした。",
                "next":"./oko.html#slide=3",
                "value" : ""
            },{
                "process":1,
                "name": "input2",
                "title": "観察/分析",
                "supp":"何がよくなかったでしょう？",
                "preface":"直接の原因は",
                "example":"昨日タイマーを設定し忘れたこと",
                "afterword":"にあります。",
                "next":"./oko.html#slide=4",
                "value" : ""
            },{
                "process":2,
                "name": "input2",
                "title": "判断",
                "supp":"何がよくなかったでしょう？",
                "preface":"このようなことが２度と起こらないよう",
                "example":"再発防止に努めます。",
                "afterword":"誠に申し訳ございませんでした。",
                "next":"./oko.html#slide=5",
                "value" : "再発防止に努めます。"
            }
        ]
    },
    "gekioko.html" :{
        "params" :  {
            "title" : "始末書自動作成システム",
            "description" : "真面目に始末書を書かなければならないとき、面倒な始末書をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
            "favicon" : "/static/チャット.png",
            "img": "http://apologagent.short-tips.info/static/thumbnail.png",
            "sample" : """この度は（一時間以上も遅刻）してしまい、大変申し訳ございませんでした。
皆様に多大なご迷惑をおかけしたことを申し上げます。
直接の原因は（アラームを設定し忘れた）ことが原因です。
今後はこのようなことが２度と起きぬよう 、再発防止に努めます。
てへぺろ〜！""",
            "volume":"4"
        },"transition" : [
            {
                "inputtype" : "date",
                "process":0,
                "name": "input1",
                "title": "時間",
                "supp":"いつ",
                "preface":"私は、",
                "example":"2021年1月10日12時30分",
                "afterword":"頃、",
                "next":"./gekioko.html#slide=3",
                "value" : "2022/01/15 10:40"
            },
            {
                "inputtype" : "text",
                "process":1,
                "name": "input2",
                "title": "業務",
                "supp":"何をしている時",
                "preface":"",
                "example":"社有車の運転中に、",
                "afterword":"",
                "next":"./gekioko.html#slide=4",
                "value" : ""
            },
            {
                "inputtype" : "text",
                "process":2,
                "name": "input3",
                "title": "結論",
                "supp":"あなたは何をやらかしました？",
                "preface":"",
                "example":"前方不注意により車を壁に追突させ破損させてしまいました。",
                "afterword":"",
                "next":"./gekioko.html#slide=5",
                "value" : ""
            },
            {
                "inputtype" : "text",
                "process":3,
                "name": "input4",
                "title": "影響",
                "supp":"誰に迷惑がかかった？",
                "preface":"この不始末のため",
                "example":"直接の上長、チームメンバー、ひいては会社全体に",
                "afterword":"迷惑をおかけしたことを深くお詫び申し上げます。",
                "next":"./gekioko.html#slide=6",
                "value" : ""
            },{
                "inputtype" : "text",
                "process":4,
                "name": "input5",
                "title": "改善",
                "supp":"どのようにすれば改善できるでしょうか",
                "preface":"今後は",
                "example":"運転に細心の注意を払い、２度とこのような事故を起こさないよう",
                "afterword":"注意いたします。大変申し訳ございませんでした。",
                "next":"./gekioko.html#slide=7",
                "value" : ""
            }
        ]
    }
}


def genPageDict(repo):
    category_list = pageInfoDict.keys()
    page_dict = {}
    for category in category_list:
        category_dict = {}
        for htmlname in Github.seach_page_list(repo, category):
            json_raw = Github.load(repo, category + "/" +htmlname)
            true_json = json.loads(json_raw)
            category_dict[htmlname] = true_json
        page_dict[category] = category_dict
    return page_dict
page_dict = genPageDict(repo)



# Create your views here.
def index(request):
    if request.GET.get("reload"):
        page_dict = genPageDict(repo)
    params = {
        "title" : "反省書自動作成システム",
        "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
        "favicon" : "/static/チャット.png",
        "img": "http://apologagent.short-tips.info/static/thumbnail.png"
    }
    return render(request,"apologagent/index.html",params)

def sitemap(request):
    return render(request,"apologagent/sitemap.xml")

def robots(request):
    return render(request, "apologagent/robots.txt")

def sample(request):
    params = {
        "title" : "反省書自動作成システム",
        "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
        "favicon" : "/static/チャット.png",
        "img": "http://apologagent.short-tips.info/static/thumbnail.png",
        "page_dict" : page_dict
    }
    return render(request, "apologagent/sample.html",params)




@csrf_exempt
def page(request, htmlname):
    if getSessionValue(request, "deleteAll") and ("transition" in request.session):
        del request.session["transition"]
    controlSessionTransition = ControlSessionTransition(request, htmlname)
    controlSessionTransition.setTransition()
    params = {}
    params.update({
        "transition": controlSessionTransition.getTransition(),
        "sentense" : controlSessionTransition.getSentense(),
        "htmlname" : htmlname
    })
    params.update(pageInfoDict[htmlname]["params"])
    if controlSessionTransition.is_last(pageInfoDict[htmlname]["params"]["volume"]):
        max_question_id = str(UniqueAPI.get_unique_id()["value"])
        json_info = json.dumps(params, ensure_ascii=False, indent=4)
        Github.upload(repo,  htmlname + "/" +max_question_id+".json", json_info)
    return render(request, f"apologagent/page/oko.html",params)


class ControlSessionTransition():
    def __init__(self, request, htmlname):
        self.request = request
        # like database
        if request.session.get("transition"):
            self.transition = request.session.get("transition")
        else:
            self.transition = pageInfoDict[htmlname]["transition"]
        self.process = self.__getProcess__()

    def getTransition(self):
        return self.transition
    
    def setTransition(self):
        transition = self.transition
        process = self.process
        if self.request.POST.get("value"):
            self.transition[self.process]["value"] = self.request.POST.get("value")

    def getSentense(self):
        buildSentense = BuildSentense(self.transition)
        return buildSentense.build()
    
    def is_last(self, number):
        return ( str(number) == str(self.__getProcess__()) )
    
    def __getProcess__(self):
        process = 0
        if self.request.POST.get("process") is None:
            pass
        else:
            process = int(self.request.POST.get("process") )
        transition = self.transition
        return process


class BuildSentense():
    def __init__(self, transition):
        super().__init__()
        self.transition = transition
        self.sentense = ""
    
    def build(self):
        self.sentense = ""
        for component in self.transition:
            for keytype in ["preface", "value", "afterword"]:
                if (keytype in component) and component[keytype]:
                    self.sentense += component[keytype]
            self.sentense += "\n"
        return self.sentense 

def getSessionValue(request, key):
    ans = request.POST.get(key)
    if ans is None:
        return ""
    return ans