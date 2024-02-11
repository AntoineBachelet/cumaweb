from django.urls import path

from . import views


app_name = "catalog"
urlpatterns = [
    path("", views.ToolListView.as_view(), name="index"),
    path("<int:tool_id>/borrow/", views.BorrowCreateView.as_view(), name="borrow_tool"),
]
