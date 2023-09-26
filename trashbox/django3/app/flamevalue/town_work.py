

import requests
from bs4 import BeautifulSoup
import time

def get_items(url, columns):
    res = requests.get(url)
    res_text = res.text
    soup = BeautifulSoup(res_text, "html.parser")
    ret = soup.find_all("div", class_="job-lst-main-cassette-wrap")
    ret.pop(0) # 最初と最後の要素は広告なので削除
    ret.pop(-1)
    for item in ret:
        rid = item.find("a", class_="job-lst-main-box-inner").get("href")
        company = item.find("h3", class_="job-lst-main-ttl-txt").text.strip()
        title = item.find("p", class_="job-lst-main-txt-lnk").text.strip()
        trs = item.select("tr.job-main-tbl-inner > td > p")
        salary = trs[0].text
        access = trs[1].text
        term = trs[2].text
        try:
            timelimit = item.select_one("p.job-lst-main-period-limit > span").text
        except AttributeError:
            timelimit = "不明"
        print("会社名:{0} タイトル:{1} 給与:{2} 交通:{3} 勤務時間:{4} 掲載終了日時:{5}" \
              .format(company, title, salary, access, term, timelimit))
    url = get_nextpage(soup)
    return  url

def get_nextpage(soup):
    try:
        url = soup.select_one("div.pager-next-btn > div.btn-wrap > a").get("href")
    except AttributeError:
        print("最後のページです")
        return
    url = "https://townwork.net" + url
    print(url)
    return url

def main():
    url = "https://townwork.net/joSrchRsltList/?fw=Swift"
    columns = ["rid", "company", "title", "salary", "access", "term", "timelimit"]
    while True:
        url = get_items(url, columns)
        time.sleep(5)
        if url is None:
            break

if __name__ == '__main__':
    main()


