from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    """Form used to create a new User"""
    # Champ de login renommé pour correspondre au modèle User
    username = forms.CharField(label="Login", max_length=100)
    first_name = forms.CharField(label="Prénom", max_length=100)
    last_name = forms.CharField(label="Nom", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
    
    def save(self, commit=True):
        # Surcharge de la méthode save pour gérer correctement le mot de passe
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hachage du mot de passe
        
        if commit:
            user.save()
        return user