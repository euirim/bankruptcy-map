from django.urls import path
from .views import search

app_name = "cases"
urlpatterns = [
    path("search/", view=search, name="search"),
]
