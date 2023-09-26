#オタク統計学
#ターゲット
from bs4 import BeautifulSoup
from urllib.request import urlopen, quote
import time

def niconicoRanking():
    url = "https://dic.nicovideo.jp/rank/hours/3/20/all/all"
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    tableObj = bsObj.find("table",{"class":"rank-list"})
    niconico_info_dict = []
    for column in tableObj.findAll("td"):
        column = column.get_text()
        print(column)
        if "\n\n" in column:
            continue
        try:
            nicoScrapy = NicoScrapy(column)
            nicoScrapy.run()
            description = nicoScrapy.getPageInfo()
        except :
            description = ""
        niconico_info_dict.append({
            "name" :column,
            "description" : description
        })
    return niconico_info_dict


class NotFoundUrl(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Scrapy():
    def __init__(self):
        self.url = ""
        self.html = ""
        self.bsObj = None
        super().__init__()
    
    def run(self):
        try:
            self.html = urlopen(self.url)
            self.bsObj = BeautifulSoup(self.html)
        except:
            return True

    




class NicoScrapy(Scrapy):
    def __init__(self,  htmlname):
        super().__init__()
        self.url = f"https://dic.nicovideo.jp/a/{ quote(htmlname)}"

    def getPageInfo(self):
        time.sleep(1)
        try:
            content = self.bsObj.find("div", {"class","a-contents"})
            for p_tag in content.findAll("p"):
                text = p_tag.get_text()
                if len(text) > 100:
                    return ""
                if "とは、" in text:
                    return text
        except Exception as error:
            return ""
        return ""

    def getWordCloud(self):
        article_bsObj = self.bsObj.find('body')
        my_list = []
        for data in article_bsObj.findAll('a'):
            my_list.append(data.text)
        return my_list


