import datetime
from django.shortcuts import render, redirect

def sitemap(request, page_list):
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d%H')
    params = {
        "pop_page_list" : page_list,
        "lastmod" : f"{dt_now.strftime('%Y')}-{dt_now.strftime('%m')}-{dt_now.strftime('%d')}T00:00:00+00:00" #"2021-07-30T13:25:37+00:00"
    }
    return render(request,"sitemap.xml", params)
