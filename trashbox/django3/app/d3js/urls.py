from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"), 
    path("robots.txt", views.robots ,name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("<htmlname>", views.page, name="page")
]

