from django.urls import path
from . import views
from . import twitter_views
from . import views_v2

urlpatterns = [
    path('', views.index , name="index"), 

    path("index.html", views_v2.index, name="index"),
    
    path("index.html", views.index ,name="pop_page"),
    path("robots.txt", views.robots ,name="robots"),
    path("sitemap.xml", views_v2.sitemap, name="sitemap"),
    path("pop_page.html", views.pop_page ,name="pop_page"),
    path("all_page.html", views.all_page ,name="all_page"),

    path("page/<htmlname>/data_loading.html", views.data_loading, name="data_loading"),
    path('page/<htmlname>/<pagetype>', views.page , name="index"),

    path("twitter_network/", twitter_views.index ,name="twitter_network"),
    path("twitter_network/<htmlname>", twitter_views.page ,name="twitter_network"),
    #path("sitemap.xml", views.sitemap, name="sitemap"),
    #path("robots.txt", views.robots, name="robots"),
    #path("page/<htmlname>", views.page , name="page")
]

