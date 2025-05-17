"""Unit tests for users application"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, CustomUserEditForm

# Models

# Forms
class CustomUserCreationFormTest(TestCase):
    """Tests unitaires pour le formulaire de création d'utilisateur"""

    def test_form_fields(self):
        """Vérifie si les champs du formulaire sont corrects"""
        form = CustomUserCreationForm()
        self.assertTrue("username" in form.fields)
        self.assertTrue("first_name" in form.fields)
        self.assertTrue("last_name" in form.fields)
        self.assertTrue("email" in form.fields)
        self.assertTrue("password1" in form.fields)
        self.assertTrue("password2" in form.fields)
        self.assertTrue("is_staff" in form.fields)
        self.assertTrue("is_superuser" in form.fields)

    def test_empty_form_validation(self):
        """Vérifie si un formulaire vide est rejeté"""
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())

        # Vérifie les erreurs requises
        self.assertIn("username", form.errors)
        self.assertIn("This field is required.", form.errors["username"][0])
        self.assertIn("password1", form.errors)
        self.assertIn("This field is required.", form.errors["password1"][0])
        self.assertIn("password2", form.errors)
        self.assertIn("This field is required.", form.errors["password2"][0])

        # Les champs facultatifs ne devraient pas générer d'erreurs
        self.assertNotIn("first_name", form.errors)
        self.assertNotIn("last_name", form.errors)
        self.assertNotIn("email", form.errors)
        self.assertNotIn("is_staff", form.errors)
        self.assertNotIn("is_superuser", form.errors)

    def test_password_mismatch(self):
        """Vérifie si des mots de passe différents sont rejetés"""
        form_data = {
            'username': 'testuser',
            'password1': 'complex_password123',
            'password2': 'different_password123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        # Vérifiez le message d'erreur spécifique pour les mots de passe non correspondants
        self.assertIn("The two password fields didn’t match.", str(form.errors['password2']))

    def test_valid_form(self):
        """Vérifie si un formulaire valide est accepté"""
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
            'is_staff': True,
            'is_superuser': False
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_with_permissions(self):
        """Vérifie si les permissions sont correctement définies lors de la création d'un utilisateur"""
        form_data = {
            'username': 'testuser',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
            'is_staff': True,
            'is_superuser': False
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Enregistrer l'utilisateur
        user = form.save()
        
        # Vérifier que les permissions ont été correctement enregistrées
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.username, 'testuser')


class CustomUserEditFormTest(TestCase):
    """Tests unitaires pour le formulaire de modification d'utilisateur"""
    
    def setUp(self):
        """Crée un utilisateur pour les tests"""
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existing_password123'
        )

    def test_form_fields(self):
        """Vérifie si les champs du formulaire sont corrects"""
        form = CustomUserEditForm(instance=self.user)
        self.assertTrue("username" in form.fields)
        self.assertTrue("first_name" in form.fields)
        self.assertTrue("last_name" in form.fields)
        self.assertTrue("email" in form.fields)
        self.assertTrue("is_staff" in form.fields)
        self.assertTrue("is_superuser" in form.fields)
        # Vérifie que le champ password n'est pas dans le formulaire d'édition
        self.assertFalse("password" in form.fields)
        self.assertFalse("password1" in form.fields)
        self.assertFalse("password2" in form.fields)

    def test_empty_form_validation(self):
        """Vérifie si un formulaire vide est rejeté"""
        form = CustomUserEditForm(data={}, instance=self.user)
        self.assertFalse(form.is_valid())

        # Vérifie les erreurs requises
        self.assertIn("username", form.errors)
        self.assertIn("This field is required.", form.errors["username"][0])

        # Les champs facultatifs ne devraient pas générer d'erreurs
        self.assertNotIn("first_name", form.errors)
        self.assertNotIn("last_name", form.errors)
        self.assertNotIn("email", form.errors)
        self.assertNotIn("is_staff", form.errors)
        self.assertNotIn("is_superuser", form.errors)

    def test_valid_form(self):
        """Vérifie si un formulaire valide est accepté"""
        form_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'is_staff': True,
            'is_superuser': True
        }
        form = CustomUserEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_user_update_with_permissions(self):
        """Vérifie si les permissions sont correctement mises à jour"""
        # Modifier l'utilisateur
        form_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'is_staff': True,
            'is_superuser': True
        }
        form = CustomUserEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
        # Enregistrer les modifications
        updated_user = form.save()
        
        # Vérifier que les informations ont été correctement mises à jour
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'User')
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertTrue(updated_user.is_staff)
        self.assertTrue(updated_user.is_superuser)
        
        # Vérifier que l'instance est bien mise à jour dans la base de données
        refreshed_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(refreshed_user.username, 'updateduser')
        self.assertTrue(refreshed_user.is_staff)
        self.assertTrue(refreshed_user.is_superuser)

    def test_username_unique_validation(self):
        """Vérifie si la validation d'unicité du nom d'utilisateur fonctionne"""
        # Créer un autre utilisateur avec un nom d'utilisateur différent
        User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='another_password123'
        )
        
        # Essayer de changer le nom d'utilisateur pour un nom qui existe déjà
        form_data = {
            'username': 'anotheruser',  # Ce nom d'utilisateur existe déjà
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        }
        form = CustomUserEditForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('A user with that username already exists.', str(form.errors['username']))

# Views
class UsersViewTest(TestCase):
    """Unit tests for the views"""

    list_urls = [
        ["/users/login/", "users:login", {}, "users/login.html"],
        ["/users/create/", "users:createUser", {}, "users/createUser.html"],
        ["/users/list/", "users:listUser", {}, "users/user_list.html"],
        ["/users/2/edit/", "users:userEdit", {"pk": 2}, "users/createUser.html"],
        ["/users/2/delete/", "users:userDelete", {"pk": 2}, "users/user_confirm_delete.html"],
    ]
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username="superuser", password="superpassword")
        test_user = User.objects.create_user(username="testuser", password="testpassword", id=2)

    
    def setUp(self):
        # Log in the user before each test
        login_successful = self.client.login(username="superuser", password="superpassword")
        self.assertTrue(login_successful)

    def test_view_url_exists_at_desired_location(self):
        """Test if url exist"""
        for url_path, _, _, _ in self.list_urls:
            response = self.client.get(url_path)
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test if URL is avalable with its name"""
        for _, url_name, kwargs_dict, _ in self.list_urls:
            response = self.client.get(reverse(url_name, kwargs=kwargs_dict))
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test if view is using the right template"""
        for _, url_name, kwargs_dict, template in self.list_urls:
            response = self.client.get(reverse(url_name, kwargs=kwargs_dict))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
