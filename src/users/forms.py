from django import forms

class CreateUserForm(forms.Form):
    lastname = forms.CharField(label="Nom", max_length=100)
    firstname = forms.CharField(label="Prénom", max_length=100)
    login = forms.CharField(label="Login", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe",widget=forms.PasswordInput())