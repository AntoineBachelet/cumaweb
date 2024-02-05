from django.contrib.auth.models import User
from django.db import models


# Create your models here.


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
    image = models.ImageField(upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class BorrowTool(models.Model):
    """
    Stores a borrowing of a tool, related to :model:`auth.User` and :model:`AgriculturalTool`.
    """

    # a tool,
    # a user borrowing the tool,
    # a date of borrowing,
    # a number of hours of borrowing
    id = models.AutoField(primary_key=True)
    tool = models.ForeignKey(AgriculturalTool, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_borrow = models.DateTimeField(auto_now_add=True)
    time_borrow = models.IntegerField()
