from django.shortcuts import render
from .sentense_class import InputText, Choice
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
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



class ActionFactory():
    def __init__(self):
        super().__init__()
    
    def getAction(self, char, target):
        if char == "u":
            return UpdateAction(target)
        elif char=="d":
            return DeleteAction(target)


pageInfoDict = {
    "oko.html" :{
        "params" :  {
            "title" : "反省書自動作成システム",
            "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
            "favicon" : "/static/チャット.png",
            "img": "http://apologagent.short-tips.info/static/thumbnail.png"
        },"transition" : [{
                "process":"1",
                "name": "input1",
                "title": "結論",
                "supp":"あなたは何をやらかしました？",
                "preface":"この度は",
                "example":"定例会議に15分以上も遅刻してしまい",
                "afterword":"、申し訳ございませんでした。",
                "next":"./oko.html#slide=3"
            },{
                "process":"2",
                "name": "input2",
                "title": "原因",
                "supp":"何がよくなかったでしょう？",
                "preface":"直接の原因は",
                "example":"昨日タイマーを設定し忘れたこと",
                "afterword":"にあります。",
                "next":"./oko.html#slide=4"
            }
        ]
    },
    "gekioko.html" :{
        "params" :  {
            "title" : "反省書自動作成システム",
            "description" : "面倒な反省文をあなたの代わりに作ります。遅刻した時、寝坊した時、居眠りしてしまった時に、どうぞ。",
            "favicon" : "/static/チャット.png",
            "img": "http://apologagent.short-tips.info/static/thumbnail.png",
            "volume":"5"
        },"transition" : [
            {
                "inputtype" : "date",
                "process":"1",
                "name": "input1",
                "title": "時間",
                "supp":"いつ",
                "preface":"私は、",
                "example":"2021年1月10日12時30分",
                "afterword":"頃、",
                "next":"./gekioko.html#slide=1"
            },
            {
                "inputtype" : "text",
                "process":"2",
                "name": "input2",
                "title": "業務",
                "supp":"何をしている時",
                "preface":"",
                "example":"社有車の運転中に、",
                "afterword":"",
                "next":"./gekioko.html#slide=2"
            },
            {
                "inputtype" : "text",
                "process":"3",
                "name": "input3",
                "title": "結論",
                "supp":"あなたは何をやらかしました？",
                "preface":"",
                "example":"前方不注意により車を壁に追突させ破損させてしまいました。",
                "afterword":"",
                "next":"./gekioko.html#slide=3"
            },
            {
                "inputtype" : "text",
                "process":"4",
                "name": "input4",
                "title": "影響",
                "supp":"誰に迷惑がかかった？",
                "preface":"この不始末のため",
                "example":"直接の上長、チームメンバー、ひいては会社全体に",
                "afterword":"迷惑をおかけしたことを深くお詫び申し上げます。",
                "next":"./gekioko.html#slide=4"
            },{
                "inputtype" : "text",
                "process":"5",
                "name": "input5",
                "title": "改善",
                "supp":"どのようにすれば改善できるでしょうか",
                "preface":"今後は",
                "example":"運転に細心の注意を払い、２度とこのような事故を起こさないよう",
                "afterword":"注意いたします。大変申し訳ございませんでした。",
                "next":"./gekioko.html#slide=4"
            }
        ]
    }
}








                
actionFactory = ActionFactory()
@csrf_exempt
def page(request, htmlname):
    session = request.session

    pageInfo = pageInfoDict[htmlname]
    params = pageInfo["params"]
    value = getSessionValue(request, "deleteAll")
    if len(value) > 1 and ("transition" in session):
        del session["transition"]

    #新規作成
    if 'transition' not in session:
        #2
        transition = pageInfo["transition"]
        request.session["transition"] = transition
    
    transition = request.session["transition"]
    pageContentList = []
    for component in transition:
        for action in [ UpdateAction(component), DeleteAction(component)]:
            value = getSessionValue(request, component["name"] + "-" + action.char)
            component = action.run(value)
        pageContentList.append(component)
    request.session["transition"] = transition

    buildSentense = BuildSentense(transition)
    params.update({
        "pageContentList":pageContentList,
        "sentense" : buildSentense.build()
    })
    return render(request, f"apologagent/page/{htmlname}",params)



def html_sample(request, htmlname):
    return render(request, f"apologagent/sample/{htmlname}")






import random
class BuildSentense():
    def __init__(self, transition):
        super().__init__()
        self.transition = transition
        self.sentense = ""
    
    def build(self):
        self.sentense = ""
        for component in self.transition:
            for keytype in ["preface", "value", "afterword"]:
                if keytype in component:
                    self.sentense += component[keytype]
            self.sentense += "\n"
        self.sentense +=   self.decoration()
        return self.sentense 
    
    def decoration(self):
        choiceList = ["""このようなことが２度と起こらないよう、再発防止に努めます。
誠に申し訳ございませんでした。""",
        "二度と同じミスを犯さぬよう細心の注意を払う所存です。本当に申し訳ございませんでした。"]
        choice = random.choice(choiceList)
        return choice


class Action():
    def __init__(self, infodict):
        self.infodict = infodict
        super().__init__()
    def check(self, value):
        if len(value) > 1:
            return True
        return False
    def run(self):
        pass

class DeleteAction(Action):
    def __init__(self, infodict):
        super().__init__(infodict)
        self.char = "d"
    def run(self, value):
        if self.check(value):
            del self.infodict["value"]
        return self.infodict


class UpdateAction(Action):
    def __init__(self, infodict):
        super().__init__(infodict)
        self.char = "u"
    def run(self, value):
        if self.check(value):
            self.infodict["value"] = value
        return self.infodict







def getSessionValue(request, key):
    ans = request.POST.get(key)
    if ans is None:
        return ""
    return ans


def saveSessionValue(request, key, value):
    request.session[key] = value