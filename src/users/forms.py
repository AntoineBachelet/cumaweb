from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """Formulaire personnalisé pour la création d'utilisateur"""
    
    # Ajout des champs is_staff et is_superuser
    is_staff = forms.BooleanField(
        required=False, 
        label="Statut Staff",
        help_text="Permet à l'utilisateur d'accéder à l'interface d'administration."
    )
    is_superuser = forms.BooleanField(
        required=False, 
        label="Statut Superutilisateur",
        help_text="Donne tous les droits à l'utilisateur sans avoir à les attribuer explicitement."
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nom d\'utilisateur',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse e-mail',
            'password1': 'Mot de passe',
        }
        help_texts = {
            'username': 'Requis. 150 caractères maximum. Uniquement des lettres, chiffres et @/./+/-/_.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes Bootstrap aux champs de mot de passe
        if 'password1' in self.fields:
            self.fields['password1'].help_text = 'Le mot de passe doit contenir au moins 8 caractères, doit être un mélange de lettres et de chiffres et ne peut pas être similaire à une autre des informations enregistrées.'
            self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        if 'password2' in self.fields:
            self.fields['password2'].help_text = 'Le mot de passe doit être identique à celui saisi dans le champ précédent.'
            self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data.get('is_staff', False)
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        if commit:
            user.save()
        return user


class CustomUserEditForm(UserChangeForm):
    """Formulaire personnalisé pour la modification d'utilisateur"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'username': 'Requis. 150 caractères maximum. Uniquement des lettres, chiffres et @/./+/-/_.',
            'is_staff': 'Permet à l\'utilisateur d\'accéder à l\'interface d\'administration.',
            'is_superuser': 'Donne tous les droits à l\'utilisateur sans avoir à les attribuer explicitement.',
        }
    
    # Supprimez le lien vers le changement de mot de passe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')