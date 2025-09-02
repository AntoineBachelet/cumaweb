from django.contrib.auth.models import User
from django.db import models


class AgriculturalTool(models.Model):
    """
    Stores an agricultural tool, related to :model:`auth.User`.
    """

    # tools
    # a name, a description,
    # an illustration,
    # a user in charge of the tool (always a user of the system)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", default=None, blank=True, null=True)
    # when the user is delete, it is set to null
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="manager_tool")


class BorrowTool(models.Model):
    """
    Stores a borrowing of a tool, related to :model:`auth.User` and :model:`AgriculturalTool`.
    """

    # a tool,
    # a user borrowing the tool,
    # a date of borrowing, default to the current date
    # a number of hours of borrowing
    id = models.AutoField(primary_key=True)
    tool = models.ForeignKey(AgriculturalTool, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_borrow = models.DateField()
    start_time_borrow = models.FloatField(help_text="Heures du matériel au début de l'emprunt")
    end_time_borrow = models.FloatField(help_text="Heures du matériel à la fin de l'emprunt")
    comment = models.TextField(null=True, blank=True)


class ToolAccess(models.Model):
    """
    Association between users and tools to define access permissions.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tool_accesses")
    tool = models.ForeignKey(AgriculturalTool, on_delete=models.CASCADE, related_name="user_accesses")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Define a unique constraint on user and tool.
        """
        unique_together = ("user", "tool")
