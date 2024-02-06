from django.urls import path

from . import views


app_name = "catalog"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:tool_id>/", views.see_tool, name="see_tool"),
]
