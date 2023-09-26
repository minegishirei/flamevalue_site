from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Yahoo
import MyJson
import NatureLang
import datetime
import Github
from django.views.decorators.csrf import csrf_exempt

REPO_QUESTIONS = "questions"

def get_questions(request, question_id):
    page_info = Github.load(REPO_QUESTIONS, question_id)
    response = HttpResponse(json.dumps(page_info, ensure_ascii=False, indent=4), content_type='application/json; charset=UTF-8')
    return response

post_count = 10

@csrf_exempt
def post_questions(request):
    global post_count
    post_count += 4
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
        "supplement" : supplement
    }
    question_json_info = json.dumps(page_info, ensure_ascii=False, indent=4)
    Github.upload(REPO_QUESTIONS, str(post_count), str(page_info))
    response = JsonResponse(page_info)
    response['Access-Control-Allow-Origin'] = '*'
    response['Accept'] = '*/*'
    return response





import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

STRIP_WIDTH = 500
STRIP_HEIGHT = 300
FILE_FONT = '/app/question/NotoSansJP-Light.otf'

def make_ogp(text):
    # テキストを必要に応じて折り返す
    text = insert_return_v2(text)
    
    im = Image.open('/app/question/console2.png')
    # イメージデータを初期化
    #im2 = Image.new("RGB", (STRIP_WIDTH, STRIP_HEIGHT), "black")
    #im2.paste(im, (0, 0))
    draw = ImageDraw.Draw(im)

    # フォントを読み込む
    font = ImageFont.truetype(FILE_FONT, 45)
    #font = ImageFont.load_default()
    # フォントの高さを計算する
    #text_width, text_height = draw.textsize(text, font)
    text_width =0
    text_height=0
    # フォントの出力位置（画像の概ね真ん中）を計算する
    position = ((100) / 2, (STRIP_HEIGHT - text_height) / 2 - 50)
    # 元画像にテキストを合成
    draw.text(position, text, (255,255,255), font=font)

    # PNGに変換
    buffer = BytesIO()
    im.save(buffer, format="PNG")
    return buffer.getvalue()

# 文字を折り返すメソッド
# もっといい方法考えるべきだが、今回はざっくりと10文字ごとに折り返す
def insert_return(text, max_width=50):
    new_string = ""
    word_list = text.split(" ")
    row = ""
    for word in word_list:
        if len(row) >= max_width:
            new_string += ( row + "\n")
            row = ""
        else:
            row += (word + " ")
    new_string += row
    return new_string


# 文字を折り返すメソッド
# もっといい方法考えるべきだが、今回はざっくりと10文字ごとに折り返す
def insert_return_v2(text, max_width=50):
    return "\n".join(text.split("..."))

# API
def ogp(request):

    text = "サムネイル"
    if "text" in request.GET:
        text = request.GET["text"]
    binary = make_ogp(text)
    # pngを指定してHTTPのレスポンスとする
    return HttpResponse(binary, content_type='image/png')