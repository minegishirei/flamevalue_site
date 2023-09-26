from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path("dialog_uml.html", views.dialog_uml, name=''),
    path("<htmlpage>" , views.dialogue_page , name=''),
]


