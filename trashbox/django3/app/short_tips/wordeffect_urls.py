from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('buildable_index.html', views.buildable_index , name="buildable_index"),
    path("<htmlpage>" , views.wordeffect_page , name='')
]


