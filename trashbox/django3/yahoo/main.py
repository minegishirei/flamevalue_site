from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pprint


class YahooCategoryPageBs4():
    def __init__(self, bsObj):
        self.bsObj =bsObj
    
    def get_all_question(self):
        table = self.bsObj.find("div", {"id", "qa_lst"})
        if table is None:
            return []
        link_list = []
        for a_tag in table.findAll("a"):
            link = a_tag["href"]
            print(link)
            if link.startswith("https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/"):
                link_list.append(link)
        return link_list


class YahooCategoryPage():
    def __init__(self):
        self.url = "https://chiebukuro.yahoo.co.jp/category/2078297616/question/list?page={}"
    
    def collect(self, max_amount):
        url_list = []
        for i in range(1,10):
            0/0
            url = self.url.format(i)
            html = urlopen(url)
            bsObj = BeautifulSoup(html)
            yahooCategoryPageBs4 = YahooCategoryPageBs4(bsObj)
            urls = yahooCategoryPageBs4.get_all_question()
            url_list.extend(urls)
            if len(url_list) > max_amount:
                break
            time.sleep(1)
        return url_list


class YahooQuestionPageBs4():
    def __init__(self, bsObj):
        self.bsObj = bsObj
    
    def get_question(self):
        question_element = self.bsObj.find("div", {"class", "ClapLv1TextBlock_Chie-TextBlock__3X4V5"})
        return question_element.get_text()
    
    def get_answer_list(self):
        ans_elements = self.bsObj.findAll("div", {"class", "ClapLv2AnswerItem_Chie-AnswerItem__Item__1lGUu"})
        ans_text_list = []
        for ans_element in ans_elements:
            h2_element = ans_element.find("h2")
            ans_text_list.append(h2_element.get_text())
        return ans_text_list


class YahooQuestionPage():
    def __init__(self, url):
        self.url = url
    
    def collect(self):
        html = urlopen(self.url)
        bsObj = BeautifulSoup(html)
        yahooQuestionPageBs4 = YahooQuestionPageBs4(bsObj)
        text =           yahooQuestionPageBs4.get_question()
        ans_text_list =  yahooQuestionPageBs4.get_answer_list()
        return {
            "title" : text,
            "answer_list" : ans_text_list
        }




def main():
    0/0
    yahooCategoryPage = YahooCategoryPage()
    link_list = yahooCategoryPage.collect(10)
    page_info_list = []
    for url in link_list[:10]:
        0/0
        page_info_list.append(url)
        yahooQuestionPage = YahooQuestionPage(url)
        page_info_list.append( yahooQuestionPage.collect() )
    return page_info_list

