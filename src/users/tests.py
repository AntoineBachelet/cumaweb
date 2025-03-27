"""Unit tests for users application"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import CreateUserForm

# Models

# Forms
class CreateUserFormTest(TestCase):
    """Unit tests for the CreateUserForm"""

    def test_form_fields(self):
        """Test if form fields are correct"""
        form = CreateUserForm()
        self.assertTrue("last_name" in form.fields)
        self.assertTrue("first_name" in form.fields)
        self.assertTrue("email" in form.fields)
        self.assertTrue("username" in form.fields)
        self.assertTrue("password" in form.fields)

    def test_empty_form_validation(self):
        """Test if empty form is rejected"""
        form = CreateUserForm(data={})
        self.assertFalse(form.is_valid())

        self.assertIn("last_name", form.errors)
        self.assertIn("This field is required.", form.errors["last_name"][0])
        self.assertIn("first_name", form.errors)
        self.assertIn("This field is required.", form.errors["first_name"][0])
        self.assertIn("username", form.errors)
        self.assertIn("This field is required.", form.errors["username"][0])
        self.assertIn("email", form.errors)
        self.assertIn("This field is required.", form.errors["email"][0])
        self.assertIn("password", form.errors)
        self.assertIn("This field is required.", form.errors["password"][0])

        self.assertEqual(len(form.errors), 5)

# Views
class UsersViewTest(TestCase):
    """Unit tests for the views"""

    list_urls = [
        ["/users/login/", "users:login", {}, "users/login.html"],
        ["/users/create/", "users:createUser", {}, "users/createUser.html"],
    ]

    @classmethod
    def setUpTestData(cls):
        # Créer plusieurs outils pour les tests de pagination, etc.
        test_user = User.objects.create_user(username="testuser", password="testpassword")
    
    def setUp(self):
        # Log in the user before each test
        login_successful = self.client.login(username="testuser", password="testpassword")
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
