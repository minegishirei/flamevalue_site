from django.urls import path
from . import views, views_v2

urlpatterns = [
    path("", views_v2.page_list ,name="index"),
    path("index.html", views_v2.page_list ,name="index"),
    path("robots.txt", views.robots ,name="robots"),
    path("sitemap.xml", views_v2.sitemap, name="sitemap"),
    path("reload.html", views.reload, name="reload"),
    path("about.html", views.about, name="about"),
    path("search/<keyword>", views_v2.search, name="search"),
    path("<page_id>", views_v2.page , name=""),
    path("<category>/<htmlname>", views.page, name="page"),
    path("<category_name>/", views.category_page, name="page"),
]

