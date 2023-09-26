#オタク統計学
#ターゲット
from bs4 import BeautifulSoup
from urllib.request import urlopen, quote
import time



class Oreilly():
    def __init__(self, book_id):
        self.params = {}
        self.book_id = book_id
        self.oreillyScrapy = OreillyScrapy(self.book_id)
        self.params.update({
            "title" : self.oreillyScrapy.get_title(),
            "description" : self.oreillyScrapy.get_description(),
            "img" : self.oreillyScrapy.get_img(),
            "book_id" : self.book_id,
            "url" : self.oreillyScrapy.get_url()
        })
    
    def get_params(self):
        return self.params


class OreillyScrapy():
    def __init__(self, book_id):
        self.url = f"https://www.oreilly.co.jp/books/{book_id}/"
        html = urlopen(self.url)
        self.bsObj = BeautifulSoup(html)
    
    def get_title(self):
        title_obj = self.bsObj.find("h3",{"class","title"})
        return title_obj.get_text()
    
    def get_img(self):
        img_obj = self.bsObj.find("img", {"class", "cover"})
        href = img_obj["src"].replace("../../", "https://www.oreilly.co.jp/")
        #img_obj = self.bsObj.find("a", {"title" , "[cover photo]"})
        #href = img_obj["href"].replace("../../", "https://www.oreilly.co.jp/books/")

        return href
    
    def get_description(self):
        description = self.bsObj.find("p" , {"itemprop":"description"})
        return description.get_text()
    
    def get_url(self):
        return self.url

        





