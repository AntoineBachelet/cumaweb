import datetime

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


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
    # image = models.ImageField(upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


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
    time_borrow = models.TimeField()
    comment = models.TextField(null=True)


class BorrowToolForm(ModelForm):
    class Meta:
        model = BorrowTool
        fields = ["tool", "user", "date_borrow", "time_borrow", "comment"]
        widgets = {
            "date_borrow": forms.DateInput(attrs={"type": "date", "value": datetime.date.today()}),
            "time_borrow": forms.TimeInput(attrs={"type": "time", "value": "01:00"}),
            "comment": forms.Textarea(attrs={"rows": 2, "cols": 50, "placeholder": "Commentaire"}),
            "tool": forms.HiddenInput(),
        }

    def clean_date_borrow(self):
        date_borrow = self.cleaned_data["date_borrow"]
        if date_borrow > datetime.date.today():
            raise forms.ValidationError("La date ne peut pas être dans le futur")
        return date_borrow


class BorrowToolFormUser(BorrowToolForm):
    # todo: formulaire uniquement pour utilisateur
    class Meta(BorrowToolForm.Meta):
        exclude = ["user"]  # exclude the user field
