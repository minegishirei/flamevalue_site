import random

import random
def titleABTest():
    return random.choice([
        lambda name, description: {
            "title" : f"【転職】「{name}の年収って実際どうなの？」 👈",
            "description" : f"{description}"
        },lambda name, description: {
            "title" : f"【転職】{name}の年収は低い",
            "description" : f"{description}"
        }
    ])


random.choice()


def page(request, htmlname):
    name = htmlname
    param = {}
    jsonIO = JsonIO()
    if jsonIO.exists(name) and (not request.GET.get("reload") ):
        param = jsonIO.read(name)
    else:
        param = build_param(name)
        jsonIO.write(param["name"],param)
    GET_active = request.GET.get("active")
    if GET_active == "jobs":
        param.update({
            "title" : f"{name} の「求人一覧」 FlameValue",
            "description" : f"{name}株式会社の採用情報です。FlameValueは{name}の採用情報・求人情報を掲載しています。"
        })
    elif GET_active == "comments":
        param.update({
            "title" : f"{name}の「すべてのクチコミ」 FlameValue",
            "description" : f"{name}ユーザーによる「すべての開発者クチコミ」のクチコミ・評価レビュー。{name}の採用を検討されている方が、{name}の「すべての開発者クチコミ」を把握するための参考情報として、{name}を使用した開発者から「すべての開発者クチコミ」に関するクチコミを収集し掲載しています。就職・採用活動での一段深めた開発者リサーチにご活用いただけます。"
        })
    else:
        param.update(titleABTest()(name,param["qiita_comments"][0]))
    return render(request, f"jobstatic_pages/page.html", param)