"""File defining the different forms used by user application"""
from django import forms

class CreateUserForm(forms.Form):
    """Form used to create a new User"""
    lastname = forms.CharField(label="Nom", max_length=100)
    firstname = forms.CharField(label="Prénom", max_length=100)
    login = forms.CharField(label="Login", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe",widget=forms.PasswordInput())
