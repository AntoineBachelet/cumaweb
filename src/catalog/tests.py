"""Definition of unit tests of catalog application"""

import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from catalog.models import AgriculturalTool, BorrowTool
from catalog.forms import CreateToolForm, BorrowToolForm


# Models


class AgriculturalToolModelTest(TestCase):
    """Unit tests for the model of AgriculturalTool"""

    @classmethod
    def setUpTestData(cls):
        # Create user for tests
        cls.test_user = User.objects.create_user(username="testuser", password="testpassword")

        # Create tool for tests
        cls.test_tool = AgriculturalTool.objects.create(
            name="Tracteur de test",
            description="Un tracteur pour les tests unitaires",
            user=cls.test_user,
        )

    def test_name_field(self):
        """Test the name field"""
        tool = AgriculturalTool.objects.get(id=self.test_tool.id)
        self.assertEqual(tool.name, "Tracteur de test")

        # Test field label
        field_label = tool._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

        # Test max length
        max_length = tool._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_description_field(self):
        """Test the description field"""
        tool = AgriculturalTool.objects.get(id=self.test_tool.id)
        self.assertEqual(tool.description, "Un tracteur pour les tests unitaires")

        # Test field label
        field_label = tool._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_user_reference(self):
        """Test that the user reference is correct"""
        tool = AgriculturalTool.objects.get(id=self.test_tool.id)
        self.assertEqual(tool.user, self.test_user)
        self.assertEqual(tool.user.username, "testuser")

    def test_set_null_on_user_delete(self):
        """Test that when a user is deleted, the tool's user field is set to NULL"""
        # Check the tool has a user
        tool_before = AgriculturalTool.objects.get(id=self.test_tool.id)
        self.assertIsNotNone(tool_before.user)

        # Delete the user
        self.test_user.delete()

        # Check the tool still exists but its user is now NULL
        tool_after = AgriculturalTool.objects.get(id=self.test_tool.id)
        self.assertIsNone(tool_after.user)

    def test_id_auto_increment(self):
        """Test that IDs are automatically assigned and incremented"""
        first_tool_id = self.test_tool.id

        # Create a second tool
        second_tool = AgriculturalTool.objects.create(
            name="Deuxième outil",
            description="Description du deuxième outil",
            user=self.test_user,
        )

        # Check the second tool has a different (higher) ID
        self.assertGreater(second_tool.id, first_tool_id)

    def test_create_without_user(self):
        """Test that a tool can be created without a user"""
        tool_without_user = AgriculturalTool.objects.create(
            name="Outil sans utilisateur",
            description="Description d'un outil sans utilisateur assigné",
        )

        self.assertIsNone(tool_without_user.user)
        self.assertEqual(tool_without_user.name, "Outil sans utilisateur")


class BorrowToolModelTest(TestCase):
    """Unit tests for the model of BorrowTool"""

    @classmethod
    def setUpTestData(cls):
        # Create user for tests
        cls.test_user = User.objects.create_user(username="testuser", password="testpassword")

        # Create tools for tests
        cls.test_tool = AgriculturalTool.objects.create(
            id=1,
            name="Tracteur de test",
            description="Un tracteur pour les tests unitaires",
            user=cls.test_user,
        )

        cls.test_borrow = BorrowTool.objects.create(
            tool=cls.test_tool,
            user=cls.test_user,
            date_borrow=datetime.date(2025, 1, 1),
            start_time_borrow=datetime.time(8, 0, 0),
            end_time_borrow=datetime.time(12, 0, 0),
            comment="Test comment",
        )

    def test_tool_reference(self):
        """Test that the tool reference is correct"""
        borrow = BorrowTool.objects.get(id=self.test_borrow.id)
        self.assertEqual(borrow.tool, self.test_tool)
        self.assertEqual(borrow.tool.name, "Tracteur de test")

    def test_user_reference(self):
        """Test that the user reference is correct"""
        borrow = BorrowTool.objects.get(id=self.test_borrow.id)
        self.assertEqual(borrow.user, self.test_user)
        self.assertEqual(borrow.user.username, "testuser")

    def test_date_borrow_value(self):
        """Test that the borrow date is correctly stored"""
        borrow = BorrowTool.objects.get(id=self.test_borrow.id)
        self.assertEqual(borrow.date_borrow, datetime.date(2025, 1, 1))

    def test_start_time_borrow_value(self):
        """Test that the start borrow time is correctly stored"""
        borrow = BorrowTool.objects.get(id=self.test_borrow.id)
        self.assertEqual(borrow.start_time_borrow, datetime.time(8, 0, 0))

    def test_end_time_borrow_value(self):
        """Test that the end borrow time is correctly stored"""
        borrow = BorrowTool.objects.get(id=self.test_borrow.id)
        self.assertEqual(borrow.end_time_borrow, datetime.time(12, 0, 0))

    def test_comment_value(self):
        """Test that the comment is correctly stored"""
        borrow = BorrowTool.objects.get(id=self.test_borrow.id)
        self.assertEqual(borrow.comment, "Test comment")

    def test_cascade_delete_tool(self):
        """Test that when a tool is deleted, its borrows are also deleted"""
        # Count borrows before deleting the tool
        borrow_count_before = BorrowTool.objects.count()
        self.assertEqual(borrow_count_before, 1)

        # Delete the tool
        self.test_tool.delete()

        # Count borrows after deletion
        borrow_count_after = BorrowTool.objects.count()
        self.assertEqual(borrow_count_after, 0)

    def test_cascade_delete_user(self):
        """Test that when a user is deleted, their borrows are also deleted"""
        # Count borrows before deleting the user
        borrow_count_before = BorrowTool.objects.count()
        self.assertEqual(borrow_count_before, 1)

        # Delete the user
        self.test_user.delete()

        # Count borrows after deletion
        borrow_count_after = BorrowTool.objects.count()
        self.assertEqual(borrow_count_after, 0)


# Forms
class CreateToolFormTest(TestCase):
    """Unit tests for the CreateToolForm"""

    def test_form_fields(self):
        """Test if form fields are correct"""
        form = CreateToolForm()
        self.assertTrue("name" in form.fields)
        self.assertTrue("description" in form.fields)
        self.assertTrue("user" in form.fields)
        self.assertTrue("image" in form.fields)

    def test_empty_form_validation(self):
        """Test if empty form is rejected"""
        form = CreateToolForm(data={})
        self.assertFalse(form.is_valid())

        self.assertIn("name", form.errors)
        self.assertIn("This field is required.", form.errors["name"][0])
        self.assertIn("description", form.errors)
        self.assertIn("This field is required.", form.errors["description"][0])
        self.assertIn("user", form.errors)
        self.assertIn("This field is required.", form.errors["user"][0])

        self.assertEqual(len(form.errors), 3)


class BorrowToolFormTest(TestCase):
    """Unit tests for the BorrowToolForm"""

    def test_form_fields(self):
        """Test if form fields are correct"""
        form = BorrowToolForm()
        self.assertTrue("tool" in form.fields)
        self.assertTrue("user" in form.fields)
        self.assertTrue("date_borrow" in form.fields)
        self.assertTrue("start_time_borrow" in form.fields)
        self.assertTrue("end_time_borrow" in form.fields)
        self.assertTrue("comment" in form.fields)

    def test_empty_form_validation(self):
        """Test if empty form is rejected"""
        form = BorrowToolForm(data={})
        self.assertFalse(form.is_valid())

        self.assertIn("tool", form.errors)
        self.assertIn("This field is required.", form.errors["tool"][0])
        self.assertIn("user", form.errors)
        self.assertIn("This field is required.", form.errors["user"][0])
        self.assertIn("date_borrow", form.errors)
        self.assertIn("This field is required.", form.errors["date_borrow"][0])
        self.assertIn("start_time_borrow", form.errors)
        self.assertIn("This field is required.", form.errors["start_time_borrow"][0])
        self.assertIn("end_time_borrow", form.errors)
        self.assertIn("This field is required.", form.errors["end_time_borrow"][0])
        self.assertIn("comment", form.errors)
        self.assertIn("This field is required.", form.errors["comment"][0])

        self.assertEqual(len(form.errors), 6)

    def test_clean_date_borrow(self):
        """Test if form fields are correct"""
        form = BorrowToolForm(
            data={
                "tool": 1,
                "user": 1,
                "date_borrow": datetime.date(2050, 1, 1),
                "start_time_borrow": datetime.time(8, 0, 0),
                "start_time_borrow": datetime.time(12, 0, 0),
                "comment": "Test comment",
            }
        )
        self.assertIn("date_borrow", form.errors)
        self.assertIn("La date ne peut pas être dans le futur", form.errors["date_borrow"][0])


# Views
class ToolListViewTest(TestCase):
    """Unit tests for the views"""

    list_urls = [
        ["/catalog/", "catalog:index", {}, "catalog/index.html"],
        ["/catalog/create_tool/", "catalog:create_tool", {}, "catalog/createtoolform.html"],
        ["/catalog/1/borrow/", "catalog:borrow_tool", {"tool_id": 1}, "catalog/toolform.html"],
        ["/catalog/1/", "catalog:tool_detail", {"pk": 1}, "catalog/tooldetail.html"],
        ["/catalog/1/export/", "catalog:export_tool", {"tool_id": 1}, None],
    ]

    @classmethod
    def setUpTestData(cls):
        # Créer plusieurs outils pour les tests de pagination, etc.
        test_user = User.objects.create_user(username="testuser", password="testpassword")

        number_of_tools = 10
        for tool_id in range(number_of_tools):
            AgriculturalTool.objects.create(
                name=f"Outil {tool_id}", description=f"Description {tool_id}", user=test_user
            )

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
            if template:
                self.assertTemplateUsed(response, template)

    def test_export_functionality(self):
        """Test if the export function returns the correct response with Excel file"""
        # First create some borrow records for testing
        test_user = User.objects.get(username="testuser")
        test_tool = AgriculturalTool.objects.get(id=1)

        # Create a few borrows
        BorrowTool.objects.create(
            tool=test_tool,
            user=test_user,
            date_borrow=datetime.date.today(),
            start_time_borrow=datetime.time(8, 0, 0),
            end_time_borrow=datetime.time(12, 0, 0),
            comment="Test borrow",
        )

        # Test the export URL
        response = self.client.get(reverse("catalog:export_tool", kwargs={"tool_id": 1}))

        # Check if response has the correct status code
        self.assertEqual(response.status_code, 200)

        # Verify the content type is correct for an Excel file
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
