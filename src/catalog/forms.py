"""Definition of the forms of catalog application"""

import datetime

from django import forms
from django.forms import ModelForm

from .models import BorrowTool, AgriculturalTool


class BorrowToolForm(ModelForm):
    """Form used to create a new borrow entry"""

    class Meta:
        """Main definition of form"""

        model = BorrowTool
        fields = ["tool", "user", "date_borrow", "time_borrow", "comment"]
        widgets = {
            "date_borrow": forms.DateInput(attrs={"type": "date", "value": datetime.date.today()}),
            "time_borrow": forms.TimeInput(attrs={"type": "time", "value": "01:00"}),
            "comment": forms.Textarea(attrs={"rows": 2, "cols": 50, "placeholder": "Commentaire"}),
            "tool": forms.HiddenInput(),
        }

    def clean_date_borrow(self):
        """Validation function for date of borrow"""
        date_borrow = self.cleaned_data["date_borrow"]
        if date_borrow > datetime.date.today():
            raise forms.ValidationError("La date ne peut pas être dans le futur")
        return date_borrow


class CreateToolForm(ModelForm):
    """Form used to create a new AgriculturalTool entry"""

    class Meta:
        """Main definition of form"""

        model = AgriculturalTool
        fields = ["name", "description", "user"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2, "cols": 50, "placeholder": "Commentaire"}),
        }


class BorrowToolFormUser(BorrowToolForm):
    """Form used to create a new borrow entry for the connected user"""

    # todo: formulaire uniquement pour utilisateur
    class Meta(BorrowToolForm.Meta):
        """Main definition of form"""

        exclude = ["user"]  # exclude the user field
