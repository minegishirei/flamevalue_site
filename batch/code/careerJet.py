from functools import reduce
from careerjet_api import CareerjetAPIClient
import pprint
import datetime

def getCareerJet(q):
    cj  =  CareerjetAPIClient("ja_JP");
    def fetch(start_num = 1):
        return cj.search({
            'start_num'   : start_num,
            'pagesize'    : 99,
            'contractperiod': 'f',
            'location'    : 'japan',
            'keywords'    : q,
            'affid'       : "2fe9505824da669b63789f957def6e26",
            'user_ip'     : '11.22.33.44',
            'url'         : 'http://www.example.com/jobsearch?q=python&l=london',
            'user_agent'  : 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
        })
    def clear_jobs(jobs):
        black_list = ["株式会社ハイウェル", "バリューアークコンサルティング株式会社"]
        return list( filter(lambda row: row["company"] not in black_list,jobs) )
    result_json = fetch()
    result_json = {
        "jobs"  : clear_jobs(result_json["jobs"]) + clear_jobs(fetch(200)["jobs"]) ,
        "hits"  : result_json["hits"]
    }
    return result_json


def mock_getCareerJet():
    return test

def clear_jnet(origin):
    return list(filter(lambda x: ("salary_min" in x ) and ("salary_max" in x), origin))

def row_converter(origin):
    return [ row_c(row) for row in origin]

def row_c(row):
    ods = 10000
    if "year" in row["salary"]:
        ods = 10000
    elif "hour" in row["salary"]:
        ods = int(10000/(1040))
    else:
        ods = int(10000/12)
    new_row = {
            "会社名" : row["company"],
            "規模" : int(int(row["salary_max"])/ods),
            "年収" : int(int(row["salary_min"])/ods),
            "残業時間" : int(int(row["salary_max"])/ods),
            "リモート率" : (100 if remotework_checker(row) else 0),
            "年齢": 30,
            "日付" : datetime.datetime.strptime(row["date"], '%a, %d %b %Y %H:%M:%S GMT').strftime("%Y-%m-%d")
        } 
    return new_row

def remotework_checker(row):
    return ("在宅" in row["description"]) or ("リモート" in row["description"]) or ("在宅" in row["title"]) or ("リモート" in row["title"])