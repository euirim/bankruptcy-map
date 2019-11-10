from django.urls import path
from .views import search, CaseDetail

app_name = "cases"
urlpatterns = [
    path("search/", view=search, name="search"),
    path("<int:pk>/", view=CaseDetail.as_view(), name="detail"),
    path("/", view=search, name="search"),
]
