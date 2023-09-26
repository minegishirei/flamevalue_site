from django.urls import path
from . import views, views_v2, views_api
urlpatterns = [
    path("", views.index ,name="index"),
    path("robots.txt", views.robots, name="reload"),
    path("site", views_v2.sitemap, name="pop_page"),
    path("<html_name>", views_v2.html_page, name="main"),
    path("questions/", views_v2.questions, name="main"),
    path("questions/<page_id>", views_v2.main, name="main"),

    path("post_question/", views_v2.main, name="main"),

    path("api/get_questions/<question_id>", views_api.get_questions, name="main"),
    path("api/post_questions/", views_api.post_questions, name="main"),
    path("api/ogp/", views_api.ogp, name="text"),

    path("index.html", views.sitemap ,name="pop_page"),
    path("site", views.sitemap, name="pop_page"),
    path("<category>/<yahoo_id>", views.page, name="page"),
    path("<category>/", views.category_list, name="category")
]
