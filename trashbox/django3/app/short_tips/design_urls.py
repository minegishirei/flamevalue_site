from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path("table_index.html", views.table_index , name="table_index"),
    path("<htmlpage>" , views.design_page , name=''),
]


