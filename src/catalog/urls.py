from django.urls import path

from . import views


app_name = "catalog"
urlpatterns = [
    path("", views.ToolListView.as_view(), name="index"),
    path("create_tool", views.ToolCreateView.as_view(), name="create_tool"),
    path("<int:tool_id>/borrow/", views.BorrowCreateView.as_view(), name="borrow_tool"),
]
