from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import CreateUserForm

# Models

# Forms
class CreateUserFormTest(TestCase):
    """Unit tests for the CreateUserForm"""

    def test_form_fields(self):
        """Test if form fields are correct"""
        form = CreateUserForm()
        self.assertTrue("lastname" in form.fields)
        self.assertTrue("firstname" in form.fields)
        self.assertTrue("email" in form.fields)
        self.assertTrue("login" in form.fields)
        self.assertTrue("password" in form.fields)

    def test_empty_form_validation(self):
        """Test if empty form is rejected"""
        form = CreateUserForm(data={})
        self.assertFalse(form.is_valid())

        self.assertIn("lastname", form.errors)
        self.assertIn("This field is required.", form.errors["lastname"][0])
        self.assertIn("firstname", form.errors)
        self.assertIn("This field is required.", form.errors["firstname"][0])
        self.assertIn("login", form.errors)
        self.assertIn("This field is required.", form.errors["login"][0])
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
