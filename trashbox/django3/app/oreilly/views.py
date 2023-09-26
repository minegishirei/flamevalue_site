#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pprint
import datetime
import sys
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Github
import MyJson
import os
import threading
import random
import json
import Oreilly
from django.views.decorators.csrf import csrf_exempt


from DAO import DAO, InsertableDAO, TableCreatableDAO, CmdDAO, create_newTable, DatabaseCreatableDAO



site_title = "オライリー書籍一覧"
site_description = "オライリー書籍のファンサイトです。おしゃれでシンプルでなおかつ美しい表紙を取り揃えました。オライリージャパンはPythonから始まりゼロトラストネットワーク,プロジェクトマネジメントの手法まで高レベルな範囲までをカバーしてます。"
repo = "oreilly"
repo_com = "oreilly_com"

oreilly_favicon = "/static/oreilly/saru.png"


all_oreilly_title = "オライリー大図鑑"
all_oreilly_description = "オライリー書籍のファンサイトです。おしゃれでシンプルでなおかつ美しい表紙を取り揃えました。オライリージャパンはPythonから始まりゼロトラストネットワーク,プロジェクトマネジメントの手法まで高レベルな範囲までをカバーしてます。"


tag_list_file_path = "./taglist.json"

class SwitchPage():
    def __init__(self):
        pass

    def main(self, request, htmlpage=""):
        if "--" in htmlpage:
            return registar(request, htmlpage)
        elif "index.html" == htmlpage:
            return self.index(request)
        elif "buildable_index.html" == htmlpage:
            return self.buildable_index(request)
        elif "robots.txt" == htmlpage:
            return self.robots(request)
        elif htmlpage.endswith(".xml"):
            return self.sitemap(request, htmlpage)
        else:
            return self.elsepage(request, htmlpage)

    def index(self, request):
        if request.GET.get("reload"):
            reload_page()
        indexParamFactory  = IndexParamFactory()
        params = indexParamFactory.build()
        return render(request, "oreilly/index.html", params)

    def all_oreilly(self, request):
        indexParamFactory  = AllPageParamFactory()
        params = indexParamFactory.build()
        return render(request, "oreilly/all_oreilly.html", params)

    def robots(self, request):
        return render(request, 'meta/robots.txt')

    def sitemap(self, request):
        page_list = []
        for page in PAGE_DICT_LIST:
            page_list.append("https://oreilly.short-tips.info/"+page["book_id"])
        page_list.append("https://oreilly.short-tips.info/index.html")
        page_list.append("https://oreilly.short-tips.info/all_oreilly.html")
        for page in gen_tag_list():
            page_list.append(f"https://oreilly.short-tips.info/tag_page_list/{page}")
        dt_now = datetime.datetime.now()
        params = {
            "page_list" : page_list,
            "lastmod" : f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
        }
        return render(request, f'oreilly/sitemap.xml', params)

    def table_index(self, request):
        ParamFactory = ParamFactory(request, "table_index.html")
        ParamFactory.set_lilist()
        ParamFactory.page()
        return render(request,  'table_index.html', ParamFactory.params)
    
    
    def page(self, request, htmlpage):
        if not Github.has_already_created(repo, htmlpage):
            add_to_github(htmlpage)
        
        paramFactory = PageParamFactory()
        if request.POST.get("title"):
            context = {
                'title': request.POST['title'],
                'comment': request.POST['comment'],
                'good' : 0
            }
            params = paramFactory.build( htmlpage, context)
            del request.POST["title"]
            del request.POST["comment"]
        else:
            params = paramFactory.build( htmlpage)
        
        return render(request, "oreilly/oreilly_base.html",params)
    
    def sql(self, request):
        category_name = request.get_host().split(".")[0]
        paramFactory = SQLParamFactory()
        sentence = request.POST.get("sql")
        if sentence is None:
            sentence = f"select * from {category_name}"
        params = paramFactory.build(category_name, sentence)
        return render(request, "sql.html", params)

    def get_tag_page_list(self, request, tag_name):
        factory = TagPageListFactory()
        params = factory.build(tag_name)
        return render(request, "oreilly/tag_page_list.html", params)
    
    def search_page(self, request):
        factory = SearchPageFactory()
        keyword_query = request.GET.get("keyword")
        if keyword_query and len(keyword_query) > 1:
            params = factory.build(keyword_query)
            return render(request, "oreilly/tag_page_list.html", params)
        else:
            return redirect("/")

    def get_tag_list(self, request):
        factory = SearchPageFactory()
        params = factory.build(keyword)

        return render(request, "oreilly/tag_page_list.html", params)
    


switchPage = SwitchPage()

@csrf_exempt
def page(request, htmlpage):
    if not Github.has_already_created(repo, htmlpage):
        add_to_github(htmlpage)
    paramFactory = PageParamFactory()
    if request.POST.get("title"):
        context = {
            'title': request.POST['title'],
            'comment': request.POST['comment'],
            'good' : 0
        }
        params = paramFactory.build( htmlpage, context)
        context = False
    else:
        params = paramFactory.build( htmlpage)
    
    return render(request, "oreilly/oreilly_base.html",params)


class ParamComponent():
    def __init__(self):
        self.comdict ={}
        super().__init__()
    
    def getComdict(self):
        return self.comdict


class TitleComponent(ParamComponent):
    def __init__(self, title):
        super().__init__()
        self.comdict.update({
            "title" : title 
        })

class MetaTitleComponent(ParamComponent):
    def __init__(self,  title):
        super().__init__()
        self.comdict.update({
            "title" : title 
        })


class DescriptionComponent(ParamComponent):
    def __init__(self, description):
        super().__init__()
        self.comdict.update({
            "description" : description 
        })

class FaviconComponent(ParamComponent):
    def __init__(self, favicon):
        super().__init__()
        self.comdict.update({
            "favicon" : favicon 
        })

class RelationComponent(ParamComponent):
    def __init__(self, page_name):
        super().__init__()
        target_index = 0
        rate = 5
        for i, page_dict in enumerate(PAGE_DICT_LIST):
            if page_dict["book_id"] == page_name:
                target_index = i
                break
        target_index_start  = max(target_index-rate,0)
        target_index_end    = min(target_index+rate+1, len(PAGE_DICT_LIST))
        core_relation = PAGE_DICT_LIST[target_index_start: target_index_end]
        self.comdict.update({"all_relation": core_relation})
    

class AllRelationComponent(ParamComponent):
    def __init__(self, ):
        super().__init__()
        self.comdict.update({"all_relation": PAGE_DICT_LIST})

class PageComponent(ParamComponent):
    def __init__(self,  page_name):
        super().__init__()
        json_str = Github.load(repo, page_name)
        myJson = MyJson.MyJson()
        self.comdict.update(myJson.read(json_str))


class PageComponentCHTitle(ParamComponent):
    def __init__(self,  page_name):
        super().__init__()
        json_str = Github.load(repo, page_name)
        myJson = MyJson.MyJson()
        params = myJson.read(json_str)
        params["title"] = "書籍まとめ | " + params["title"]
        self.comdict.update(params)



class CommentComponent(ParamComponent):
    def __init__(self,  page_name, new_dict=False):
        super().__init__()
        def dub_check(comment_list, new_dict):
            for old_dict in comment_list:
                if old_dict["title"] == new_dict["title"]:
                    return True
            return False

        comment_list = []
        if Github.has_already_created(repo_com, page_name):
            json_str = Github.load(repo_com, page_name)
            myJson = MyJson.MyJson()
            comment_list = myJson.read(json_str)
            if new_dict and (not dub_check(comment_list, new_dict)):
                Github.delete_page(repo_com, page_name)
                comment_list.append(new_dict)
                json_str = myJson.write(comment_list)
                Github.upload(repo_com, page_name, json_str)
        else:
            Github.upload(repo_com, page_name, str(comment_list))
        self.comdict.update({
            "comment_list" : comment_list
        })


class SQLComponent(ParamComponent):
    def __init__(self, category_name, cmd):
        super().__init__()
        with DAO(category_name) as dao:
            result = dao.run(cmd)
            self.comdict.update({"all_relation": result})
            self.comdict.update({"sql" : cmd})


class TagListComponent(ParamComponent):
    def __init__(self):
        super().__init__()
        self.comdict.update({
            "tag_list": gen_tag_list()
        })

class TagPageListComponent(ParamComponent):
    def __init__(self, tag_name):
        super().__init__()
        tag_page_list = []
        with DAO("TAG_PAGE_LIST") as dao:
            result = dao.run(f'select * from TAG_PAGE_LIST where TAG_NAME = "{tag_name}"')
            for row in result:
                for page_dict in PAGE_DICT_LIST:
                    if row["BOOK_ID"] == page_dict["book_id"]:
                        tag_page_list.append(page_dict)

        self.comdict.update({
            "all_relation": tag_page_list
        })


class SearchPageComponent(ParamComponent):
    def __init__(self, keyword_str):
        keyword = keyword_str
        super().__init__()
        search_result = []
        hit_count = 0
        for page_dict in PAGE_DICT_LIST:
            ##TODO:keywordによる条件分岐
            condition = ( 
                    1!=1
                    or (keyword in page_dict["title"])
                    or (keyword.upper() in page_dict["title"])
                    or (keyword.lower() in page_dict["title"])
                    or (keyword.capitalize() in page_dict["title"])
                )
            if condition:
                hit_count += 1
                search_result.append(page_dict)
        if hit_count >= 2:
            with InsertableDAO("TAG_PAGE_LIST") as dao:
                try:
                    dao.insert(f"('{keyword}', 'xxxxxxxxxx')")
                except:
                    pass
        self.comdict.update({
            "all_relation": search_result
        })






###############################

class ParamFactory():
    def __init__(self):
        self.params = {}
        self.category_name = ""
        super().__init__()
    
    def getFactory(self, factoryType):
        pass

class IndexParamFactory(ParamFactory):
    def __init__(self):
        self.factoryType = "index"
        super().__init__()
    
    def build(self):
        componentList = [
            TitleComponent( site_title ),
            AllRelationComponent(),
            DescriptionComponent( site_description),
            FaviconComponent( oreilly_favicon ),
            TagListComponent()
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params


class AllPageParamFactory(ParamFactory):
    def __init__(self):
        self.factoryType = "index"
        super().__init__()
    
    def build(self):
        componentList = [
            TitleComponent( all_oreilly_title ),
            AllRelationComponent(),
            TagListComponent(),
            DescriptionComponent( all_oreilly_description ),
            FaviconComponent( oreilly_favicon )
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params


class PageParamFactory(ParamFactory):
    def __init__(self):
        super().__init__()
    
    def build(self,  page_name, new_dict=False):
        componentList = [
            PageComponentCHTitle(page_name),
            AllRelationComponent(),
            TagListComponent(),
            CommentComponent(page_name, new_dict),
            RelationComponent(page_name),
            FaviconComponent( oreilly_favicon )
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params


class SQLParamFactory(ParamFactory):
    def __init__(self):
        super().__init__()
    
    def build(self, category_name, cmd):
        self.category_name = category_name
        componentList = [
            MetaTitleComponent(category_name, category_name),
            SQLComponent(category_name,cmd),
            FaviconComponent( oreilly_favicon )
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params


class TagPageFactory(ParamFactory):
    def __init__(self):
        super().__init__()
    
    def build(self, tag_name):
        self.tag_name = tag_name
        componentList = [
            MetaTitleComponent("オライリー "+tag_name+"まとめ"),
            AllRelationComponent(),
            TagListComponent(),
            FaviconComponent( oreilly_favicon )
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params


class TagPageListFactory(ParamFactory):
    def __init__(self):
        super().__init__()

    def build(self, tag_name):
        self.tag_name = tag_name
        componentList = [
            MetaTitleComponent("オライリー "+tag_name+"まとめ"),
            AllRelationComponent(),
            TagListComponent(),
            TagPageListComponent(tag_name),
            FaviconComponent( oreilly_favicon )
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params
        

class SearchPageFactory(ParamFactory):
    def __init__(self):
        super().__init__()

    def build(self, keyword):
        self.keyword = keyword
        componentList = [
            MetaTitleComponent(keyword),
            AllRelationComponent(),
            SearchPageComponent(keyword),
            FaviconComponent( oreilly_favicon )
        ]
        for component in componentList:
            self.params.update(component.getComdict())
        return self.params


def add_to_github(book_id):
    oreilly = Oreilly.Oreilly(book_id)
    params = oreilly.get_params()
    myJson = MyJson.MyJson()
    Github.upload(repo, book_id, myJson.write(params))


PAGE_DICT_LIST = []
def gen_page_dict_list():
    global PAGE_DICT_LIST
    PAGE_DICT_LIST = []
    for book_id in Github.seach_page_list(repo):
        json_str = Github.load(repo, book_id)
        myJson = MyJson.MyJson()
        page_dict = myJson.read(json_str)
        with InsertableDAO("TAG_PAGE_LIST") as dao:
            for tag_name in gen_tag_list():
                condition = ( 
                    (tag_name.capitalize() in page_dict["description"]) 
                    or (tag_name.upper() in page_dict["description"])
                    or (tag_name.lower() in page_dict["description"])
                    or (tag_name in page_dict["title"])
                    or (tag_name.upper() in page_dict["title"])
                    or (tag_name.lower() in page_dict["title"])
                    or (tag_name.capitalize() in page_dict["title"])
                )
                if condition:
                    try:
                        dao.insert(f"('{tag_name}', '{book_id}')")
                    except:
                        pass

        PAGE_DICT_LIST.append({
            "title" : page_dict["title"],
            "book_id" : page_dict["book_id"],
            "img" : page_dict["img"]
        })
        
    PAGE_DICT_LIST.reverse()


def gen_tag_list():
    tag_page_list = []
    with DAO("TAG_PAGE_LIST") as dao:
        for tag_dict in dao.run(f'select DISTINCT TAG_NAME from TAG_PAGE_LIST'):
            tag_page_list.append( tag_dict["TAG_NAME"] )
    return tag_page_list


def init_dao():
    with TableCreatableDAO("TAG_PAGE_LIST", " TAG_NAME varchar(30), BOOK_ID varchar(20) ,PRIMARY KEY( TAG_NAME, BOOK_ID ) ") as dao:
        pass

def reload_page():
    init_dao()
    gen_page_dict_list()


reload_page()










