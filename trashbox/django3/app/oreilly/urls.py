from django.urls import path
from . import views
switchPage = views.SwitchPage()
urlpatterns = [
    path('', switchPage.index , name="index"),
    path("index.html" , switchPage.index , name=''),
    path("all_oreilly.html" , switchPage.all_oreilly , name=''),
    path("robots.txt", switchPage.robots, name="robots"),
    path("sitemap.xml", switchPage.sitemap , name= ""),
    path("tag_list", switchPage.get_tag_list, name="tag_list"),
    path("tag_page_list/<tag_name>", switchPage.get_tag_page_list, name="tag_page_list"),
    path("search_page", switchPage.search_page, name="search_page"),
    path("<htmlpage>" , views.page , name=''),
]


