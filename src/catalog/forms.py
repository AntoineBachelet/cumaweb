"""Definition of the forms of catalog application"""

import datetime

from django import forms
from django.forms import ModelForm
from django.db.models import Max

from .models import BorrowTool, AgriculturalTool


class BorrowToolForm(ModelForm):
    """Form used to create a new borrow entry"""

    class Meta:
        """Main definition of form"""

        model = BorrowTool
        fields = ["tool", "user", "date_borrow", "start_time_borrow", "end_time_borrow", "comment"]
        widgets = {
            "date_borrow": forms.DateInput(attrs={"type": "date", "value": datetime.date.today()}),
            "start_time_borrow": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "end_time_borrow": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "comment": forms.Textarea(attrs={"rows": 2, "cols": 50, "placeholder": "Commentaire"}),
            "tool": forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(BorrowToolForm, self).__init__(*args, **kwargs)
        if self.initial.get('tool'):
            tool_id = self.initial.get('tool').id

            latest_return = BorrowTool.objects.filter(
                tool_id=tool_id
            ).aggregate(Max('end_time_borrow'))['end_time_borrow__max']

            if latest_return:
                self.fields['start_time_borrow'].widget = forms.NumberInput(
                    attrs={"step": "0.1", "min": "0", "value": latest_return}
                )

    def clean_date_borrow(self):
        """Validation function for date of borrow"""
        date_borrow = self.cleaned_data["date_borrow"]
        if date_borrow > datetime.date.today():
            raise forms.ValidationError("La date ne peut pas être dans le futur")
        return date_borrow
    
    def clean_end_time_borrow(self):
        """Validation function for end time of borrow"""
        start_time_borrow = self.cleaned_data["start_time_borrow"]
        end_time_borrow = self.cleaned_data["end_time_borrow"]
        if end_time_borrow <= start_time_borrow:
            raise forms.ValidationError("L'heure de fin doit être supérieure à l'heure de début")
        return end_time_borrow


class CreateToolForm(ModelForm):
    """Form used to create a new AgriculturalTool entry"""

    class Meta:
        """Main definition of form"""

        model = AgriculturalTool
        fields = ["name", "description", "user", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2, "cols": 50, "placeholder": "Commentaire"}),
            "image": forms.FileInput(attrs={"accept": ".png, .jpg, .jpeg"}),
        }


class BorrowToolFormUser(BorrowToolForm):
    """Form used to create a new borrow entry for the connected user"""

    # todo: formulaire uniquement pour utilisateur
    class Meta(BorrowToolForm.Meta):
        """Main definition of form"""

        exclude = ["user"]  # exclude the user field
