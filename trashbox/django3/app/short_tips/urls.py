from django.urls import path
from . import views
from django.shortcuts import render, redirect

urlpatterns = [
    path("", views.index ,name="index"),
    path("index.html", views.index ,name="index"),
    path("robots.txt", views.robots ,name="robots"),
    path("ads.txt", (lambda request: render(request, "ads.txt") ), name="ads.txt"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("sitemap/", views.sitemap, name="s"),
    path("<category>/<htmlname>", views.page, name="page"),
    path("about.html/", views.about, name="about"),
    path("<category_name>/", views.category_page, name="page")
]

