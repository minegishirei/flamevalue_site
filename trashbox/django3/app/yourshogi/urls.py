from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name="index"), 
    path("index.html", views.index ,name="pop_page"),
    path("api/<kifu_str>/<push_str>", views.api, name="api")
    #path("robots.txt", views.robots ,name="robots"),
]

