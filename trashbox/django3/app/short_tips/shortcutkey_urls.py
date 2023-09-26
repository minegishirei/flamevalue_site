from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("robots.txt", views.robots, name="robots"),
    path("<htmlpage>" , views.shortcutkey_page , name='')
]


