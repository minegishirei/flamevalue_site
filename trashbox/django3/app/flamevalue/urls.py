from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name="index"), 
    path('login.html', views.login, name="login"),
    path('index.html', views.reverse_index , name="index"),
    path('useradmin.html', views.useradmin, name="useradmin"),
    path("sitemap", views.sitemap, name="sitemap"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("robots.txt", views.robots, name="robots"),
    path("api/candidate/", views.api_candidate, name="candidate"),
    path("ranking.html", views.ranking, name="ranking"),
    path("search.html", views.search, name="search"),
    path("compare.html", views.compare, name="compare"),
    path("<htmlname>", views.page ,name="pop_page")
]

