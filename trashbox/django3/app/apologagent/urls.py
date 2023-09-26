from django.urls import path
from . import views, views_v2
urlpatterns = [
    path('', views.index , name="index"), 
    path('index.html', views_v2.index , name="index"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("robots.txt", views.robots, name="robots"),
    path("sample.html", views_v2.sample, name="html_sample"),
    path("html_sample/<htmlname>", views.html_sample, name="html_sample"),
    path("page/<htmlname>", views_v2.page , name="page")
    #path("page_v2/<htmlname>", views_v2.page , name="page")
]




#https://webslides.tv/demos/portfolios#slide=8


