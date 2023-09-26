from django.urls import path
from . import views
switchPage = views.SwitchPage()
urlpatterns = [
    path('', switchPage.index , name="index"),
    path("index.html" , switchPage.index , name=''),
    path("all_oreilly.html" , switchPage.all_oreilly , name=''),
    path("robots.txt", switchPage.robots, name="robots"),
    path("sitemap.xml", switchPage.sitemap , name= ""),
    path("<htmlpage>" , views.page , name=''),
]


