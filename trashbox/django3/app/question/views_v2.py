from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Yahoo
import MyJson
import NatureLang
import datetime
import Github
import UniqueAPI

REPO_ANSWERS = "answers"
REPO_QUESTIONS = "questions"
global_params = {
    "site_name": "エラー解決！",
    "site_description" : "本サイトはあなたのエラーメッセージを解決に導きます。",
    "question_list" : [],
    "keyword_list" : set()
}
def rebuild_question_list():
    question_id_list = Github.seach_page_list_v2(REPO_QUESTIONS)
    page_info_list = []
    for question_id in question_id_list:
        page_info = Github.load(REPO_QUESTIONS, question_id)
        page_info_list.append(json.loads(page_info))
    global_params["question_list"] = page_info_list
rebuild_question_list()



def html_page(request, html_name):
    if "reload" in request.GET:
        rebuild_question_list()
    params = {}
    params.update({
        "title" : global_params["site_name"],
        "description" : global_params["site_description"]
    })
    return render(request, f"question_v2/{html_name}", params)


def questions(request):
    params = {}
    if ("search" in request.GET) and ( len(request.GET["search"]) >= 3):
        search = request.GET["search"]
        search_result_list = []
        for question in global_params["question_list"]:
            is_target = ( (" " + search) in str(question) ) or ( ( search + " " ) in str(question) )
            global_params["keyword_list"].add(search)
            if is_target:
                search_result_list.append(question)
        params.update({
            "question_list" : search_result_list,
            "title" : global_params["site_name"],
            "description" : global_params["site_description"],
            "keyword_list" : global_params["keyword_list"]
        })
    else:
        params.update({
            "question_list" : global_params["question_list"],
            "title" : global_params["site_name"],
            "description" : global_params["site_description"],
            "keyword_list" : global_params["keyword_list"]
        })
    return render(request, f"question_v2/blog.html", params)



def main(request, page_id):
    params = {}
    error_message_param = {}
    if "create_new_page" in request.POST:
        ## 1st. create new page
        new_error_message_param = post_questions(request)
        return redirect( "./" + str(new_error_message_param["question_id"]))
    else:
        ## 2st. find page
        new_error_message_param = get_questions(page_id)
        error_message_param = {
            "title" : new_error_message_param["error_message"][:50],
            "description" : new_error_message_param["error_message"],
            "error_message" : new_error_message_param["error_message"],
            "code" : new_error_message_param["code"],
            "supplement" : new_error_message_param["supplement"]
        }
    answer_code_param = None
    if "answer_new_page" in request.POST:
        ## 1st. create answer page
        new_answer_code_param = post_answers(request, page_id)
        return redirect( "./" + str(new_answer_code_param["question_id"]))
    else:
        try:
            answer_code_param = get_answers(page_id)
        except:
            pass
    ## 2nd. build params from page info
    params.update({
            "title" : error_message_param["title"],
            "description" : error_message_param["description"],
            "error_message_param" : error_message_param,
            "answer_code_param" : answer_code_param,
            "keyword_list" : global_params["keyword_list"]
        })
    return render(request, f"question_v2/blog_details.html", params)




def sitemap(request):
    page_list = []
    for question_id in Github.seach_page_list_v2(REPO_QUESTIONS):
        url = f"https://question.short-tips.info/questions/{question_id}"
        page_list.append(url)
    for keyword in global_params["keyword_list"]:
        url = f"https://question.short-tips.info/questions/?search={keyword}"
        page_list.append(url)
    page_list.append("https://question.short-tips.info/index.html")
    page_list.append("https://question.short-tips.info/questions/")
    page_list.append("https://question.short-tips.info/help.html")
    page_list.append("https://question.short-tips.info/post.html")
    dt_now = datetime.datetime.now()
    params = {}
    params.update({
        "page_list" : page_list,
        "last_mod"  :f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    })
    return render(request, "question/sitemap.xml", params)





def post_questions(request):
    max_question_id = str(UniqueAPI.get_unique_id()["value"])
    error_message = ""
    code = ""
    supplement = ""
    if "error_message" in request.POST:
        error_message = request.POST.get("error_message")
    if "code" in request.POST:
        code = request.POST["code"]
    if "supplement" in request.POST:
        supplement = request.POST["supplement"]
    page_info = {
        "error_message" : error_message,
        "code" : code,
        "supplement" : supplement,
        "question_id" : max_question_id
    }
    json_info = json.dumps(page_info, ensure_ascii=False, indent=4)
    Github.upload(REPO_QUESTIONS, max_question_id, json_info)
    return page_info

def get_questions(question_id):
    page_info = Github.load(REPO_QUESTIONS, question_id)
    return json.loads(page_info)



def post_answers(request, question_id):
    answer_id = question_id + "/" +str(UniqueAPI.get_unique_id()["value"])
    title = ""
    code = ""
    supplement = ""
    if "title" in request.POST:
        title = request.POST.get("title")
    if "code" in request.POST:
        code = request.POST["code"]
    if "supplement" in request.POST:
        supplement = request.POST["supplement"]
    page_info = {
        "title" : title,
        "code" : code,
        "supplement" : supplement,
        "answer_id" : answer_id,
        "question_id" : question_id
    }
    json_info = json.dumps(page_info, ensure_ascii=False, indent=4)
    Github.upload(REPO_ANSWERS, answer_id, json_info)
    return page_info

def get_answers(question_id):
    answer_id_list = Github.seach_page_list_v2(REPO_ANSWERS, question_id)
    page_info_list = []
    for answer_id in answer_id_list:
        page_info = Github.load(REPO_ANSWERS, question_id + "/" +answer_id)
        page_info_list.append(json.loads(page_info))
    return page_info_list

# HTTP Error 404: Not Found 
# Beautiful Soup urlopen python


# IncompleteRead(128834 bytes read)

"""

   url = "https://github.com/kawadasatoshi/" + repo 
    if folder is None:
        url = "https://github.com/kawadasatoshi/" + repo 
    else:
        url = f"https://github.com/kawadasatoshi/{repo}/tree/main/{folder}"
    time.sleep(1)
    html = urlopen(url)
    bsObj = BeautifulSoup(html) …
    file_list = []
    flag = False
    for row in bsObj.findAll("div", attrs={"role": "rowheader"}):
        for a_tag in row.findAll( "a",attrs={"data-pjax": "#repo-content-pjax-container"}):
            if a_tag.has_key('title'):
                file_list.append(a_tag.get_text())

"""