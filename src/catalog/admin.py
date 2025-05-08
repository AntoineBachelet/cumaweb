# Register your models here.
from django.contrib import admin

from .models import AgriculturalTool, BorrowTool, ToolAccess


admin.site.register(AgriculturalTool)
admin.site.register(BorrowTool)
admin.site.register(ToolAccess)
