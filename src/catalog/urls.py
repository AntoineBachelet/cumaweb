from django.urls import path

from . import views


app_name = "catalog"
urlpatterns = [
    path("", views.ToolListView.as_view(), name="index"),
    path("create_tool/", views.ToolCreateView.as_view(), name="create_tool"),
    path("<int:tool_id>/borrow/", views.BorrowCreateView.as_view(), name="borrow_tool"),
    path("<int:pk>/", views.ToolDetailView.as_view(), name="tool_detail"),
    path("<int:pk>/update/", views.ToolUpdateView.as_view(), name="tool_update"),
    path("<int:tool_id>/export/", views.export_to_excel, name="export_tool"),
    path("<int:tool_id>/accesses/add/", views.ToolAccessCreateView.as_view(), name="tool_access_add"),
]
