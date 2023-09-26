from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name="index"), 
    path("index.html", views.index ,name="index"),
    path("about.html", views.about ,name="about"),
    path("robots.txt", views.robots ,name="about"),
    #path("all_page.html", views.all_page ,name="all_page"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("edit/<tweet_id>", views.edit_page, name="edit"),
    path("<content_type>/", views.content_index, name="contet_ranking"),
    path("<content_type>/<htmlname>/data_loading.html", views.data_loading, name="data_loading"),
    path('<content_type>/<htmlname>/<pagetype>', views.page , name="index"),
    
    #path("page/<htmlname>/data_loading.html", views.data_loading, name="data_loading"),
    #path('page/<htmlname>/<pagetype>', views.page , name="index"),
]

