"""Definition of unit tests of catalog application"""

import datetime

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.forms import BorrowToolForm, CreateToolForm, ToolAccessForm
from catalog.models import AgriculturalTool, BorrowTool, ToolAccess

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
            start_time_borrow=140,
            end_time_borrow=150.2,
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
        self.assertEqual(borrow.start_time_borrow, 140)

    def test_end_time_borrow_value(self):
        """Test that the end borrow time is correctly stored"""
        borrow = BorrowTool.objects.get(id=self.test_borrow.id)
        self.assertEqual(borrow.end_time_borrow, 150.2)

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


class ToolAccessModelTest(TestCase):
    """Unit tests for the model of ToolAccess"""

    @classmethod
    def setUpTestData(cls):
        # Create users for tests
        cls.test_user = User.objects.create_user(username="testuser", password="testpassword")
        cls.another_user = User.objects.create_user(username="anotheruser", password="testpassword")

        # Create tools for tests
        cls.test_tool = AgriculturalTool.objects.create(
            id=1,
            name="Tracteur de test",
            description="Un tracteur pour les tests unitaires",
            user=cls.test_user,
        )
        
        cls.another_tool = AgriculturalTool.objects.create(
            id=2,
            name="Moissonneuse de test",
            description="Une moissonneuse pour les tests unitaires",
            user=cls.test_user,
        )

        # Create a tool access
        cls.test_access = ToolAccess.objects.create(
            user=cls.test_user,
            tool=cls.test_tool,
        )

    def test_user_reference(self):
        """Test that the user reference is correct"""
        access = ToolAccess.objects.get(user=self.test_user, tool=self.test_tool)
        self.assertEqual(access.user, self.test_user)
        self.assertEqual(access.user.username, "testuser")

    def test_tool_reference(self):
        """Test that the tool reference is correct"""
        access = ToolAccess.objects.get(user=self.test_user, tool=self.test_tool)
        self.assertEqual(access.tool, self.test_tool)
        self.assertEqual(access.tool.name, "Tracteur de test")

    def test_date_added_auto_now(self):
        """Test that date_added is automatically set"""
        access = ToolAccess.objects.get(user=self.test_user, tool=self.test_tool)
        self.assertIsNotNone(access.date_added)
        now = timezone.now()
        time_difference = abs((now - access.date_added).total_seconds())
        self.assertLess(time_difference, 60)

    def test_unique_constraint(self):
        """Test that the unique constraint on (user, tool) works"""
        # Attempt to create a duplicate access
        with self.assertRaises(IntegrityError):
            ToolAccess.objects.create(
                user=self.test_user,
                tool=self.test_tool,
            )

    def test_create_multiple_accesses_different_pairs(self):
        """Test that multiple accesses can be created if the (user, tool) pairs are different"""
        # Create access with same user but different tool
        access1 = ToolAccess.objects.create(
            user=self.test_user,
            tool=self.another_tool,
        )
        self.assertEqual(access1.user, self.test_user)
        self.assertEqual(access1.tool, self.another_tool)

        # Create access with same tool but different user
        access2 = ToolAccess.objects.create(
            user=self.another_user,
            tool=self.test_tool,
        )
        self.assertEqual(access2.user, self.another_user)
        self.assertEqual(access2.tool, self.test_tool)

        # Count the total number of accesses
        self.assertEqual(ToolAccess.objects.count(), 3)

    def test_related_name_from_user(self):
        """Test that the related_name from User works"""
        # Create another access for the test user
        ToolAccess.objects.create(
            user=self.test_user,
            tool=self.another_tool,
        )
        
        # Check that we can access all tools via the related_name
        user_accesses = self.test_user.tool_accesses.all()
        self.assertEqual(user_accesses.count(), 2)
        self.assertIn(self.test_tool.id, user_accesses.values_list('tool_id', flat=True))
        self.assertIn(self.another_tool.id, user_accesses.values_list('tool_id', flat=True))

    def test_related_name_from_tool(self):
        """Test that the related_name from Tool works"""
        # Create another access for the test tool
        ToolAccess.objects.create(
            user=self.another_user,
            tool=self.test_tool,
        )
        
        # Check that we can access all users via the related_name
        tool_accesses = self.test_tool.user_accesses.all()
        self.assertEqual(tool_accesses.count(), 2)
        self.assertIn(self.test_user.id, tool_accesses.values_list('user_id', flat=True))
        self.assertIn(self.another_user.id, tool_accesses.values_list('user_id', flat=True))

    def test_cascade_delete_user(self):
        """Test that when a user is deleted, their accesses are also deleted"""
        # Count accesses before deleting the user
        access_count_before = ToolAccess.objects.count()
        self.assertEqual(access_count_before, 1)

        # Delete the user
        self.test_user.delete()

        # Count accesses after deletion
        access_count_after = ToolAccess.objects.count()
        self.assertEqual(access_count_after, 0)

    def test_cascade_delete_tool(self):
        """Test that when a tool is deleted, its accesses are also deleted"""
        # Count accesses before deleting the tool
        access_count_before = ToolAccess.objects.count()
        self.assertEqual(access_count_before, 1)

        # Delete the tool
        self.test_tool.delete()

        # Count accesses after deletion
        access_count_after = ToolAccess.objects.count()
        self.assertEqual(access_count_after, 0)

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
                "start_time_borrow": 140,
                "end_time_borrow": 150,
                "comment": "Test comment",
            }
        )
        self.assertIn("date_borrow", form.errors)
        self.assertIn("La date ne peut pas être dans le futur", form.errors["date_borrow"][0])

    def test_clean_end_time_borrow(self):
        """Test if form fields are correct"""
        form = BorrowToolForm(
            data={
                "tool": 1,
                "user": 1,
                "date_borrow": datetime.date(2025, 1, 1),
                "start_time_borrow": 140,
                "end_time_borrow": 130,
                "comment": "Test comment",
            }
        )
        self.assertIn("end_time_borrow", form.errors)
        self.assertIn("L'heure de fin doit être supérieure à l'heure de début", form.errors["end_time_borrow"][0])


class ToolAccessFormTest(TestCase):
    """Unit tests for the ToolAccessForm"""
    
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.user3 = User.objects.create_user(username='user3', password='pass3')
        
        # Create a test tool
        self.tool = AgriculturalTool.objects.create(
            name="Test Tool",
            description="A test tool",
            user=self.user1  # This user is the manager
        )
        
        # Create a tool access for user2
        self.tool_access = ToolAccess.objects.create(
            tool=self.tool,
            user=self.user2
        )

    def test_form_fields(self):
        """Test if form fields are correct"""
        form = ToolAccessForm()
        self.assertTrue("user" in form.fields)

    def test_empty_form_validation(self):
        """Test if empty form is rejected"""
        form = ToolAccessForm(data={})
        self.assertFalse(form.is_valid())
        
        self.assertIn("user", form.errors)
        self.assertIn("This field is required.", form.errors["user"][0])
        
        self.assertEqual(len(form.errors), 1)

    def test_form_labels_and_help_text(self):
        """Test if form labels and help text are set correctly"""
        form = ToolAccessForm()
        self.assertEqual(form.fields["user"].label, "Utilisateur")
        self.assertEqual(form.fields["user"].help_text, "Sélectionnez l'utilisateur à qui donner accès")

    def test_user_queryset_filtering(self):
        """Test if the user queryset is properly filtered"""
        # Without passing a tool, no filtering should occur
        form = ToolAccessForm()
        self.assertEqual(form.fields["user"].queryset.count(), User.objects.count())
        
        # When passing a tool, users with existing access and managers should be excluded
        form = ToolAccessForm(tool=self.tool)
        
        # Should exclude user1 (manager) and user2 (has access already)
        filtered_queryset = form.fields["user"].queryset
        
        # Check that only user3 is in the queryset
        self.assertEqual(filtered_queryset.count(), 1)
        self.assertTrue(self.user3 in filtered_queryset)
        self.assertFalse(self.user1 in filtered_queryset)
        self.assertFalse(self.user2 in filtered_queryset)

    def test_valid_form_submission(self):
        """Test valid form submission"""
        form = ToolAccessForm(data={"user": self.user3.id}, tool=self.tool)
        self.assertTrue(form.is_valid())

    def test_already_has_access_submission(self):
        """Test submission with user that already has access"""
        # Create a form without the tool parameter so filtering doesn't occur
        form = ToolAccessForm(data={"user": self.user2.id})
        
        # Form should be valid since we're not passing the tool parameter
        # (this is just testing the form's own validation, not the view logic)
        self.assertTrue(form.is_valid())
        
        # But if we filter with the tool parameter, user2 wouldn't be in the queryset
        form = ToolAccessForm(data={"user": self.user2.id}, tool=self.tool)
        # Form should be invalid because user2 isn't in the filtered queryset
        self.assertFalse(form.is_valid())
        self.assertIn("user", form.errors)

    def test_manager_submission(self):
        """Test submission with user that is a manager"""
        # Create a form without the tool parameter so filtering doesn't occur
        form = ToolAccessForm(data={"user": self.user1.id})
        
        # Form should be valid since we're not passing the tool parameter
        self.assertTrue(form.is_valid())
        
        # But if we filter with the tool parameter, user1 wouldn't be in the queryset
        form = ToolAccessForm(data={"user": self.user1.id}, tool=self.tool)
        # Form should be invalid because user1 isn't in the filtered queryset
        self.assertFalse(form.is_valid())
        self.assertIn("user", form.errors)


# Views
class ToolListViewTest(TestCase):
    """Unit tests for the views"""

    list_urls = [
        ["/catalog/", "catalog:index", {}, "catalog/index.html"],
        ["/catalog/create_tool/", "catalog:create_tool", {}, "catalog/createtoolform.html"],
        ["/catalog/1/borrow/", "catalog:borrow_tool", {"tool_id": 1}, "catalog/toolform.html"],
        ["/catalog/1/", "catalog:tool_detail", {"pk": 1}, "catalog/tooldetail.html"],
        ["/catalog/1/export/", "catalog:export_tool", {"tool_id": 1}, None],
        ["/catalog/1/accesses/add/", "catalog:tool_access_add", {"tool_id": 1}, "catalog/tool_access_form.html"],
        ["/catalog/1/accesses/list/", "catalog:tool_access_list", {"tool_id": 1}, "catalog/tool_access_list.html"],
        ["/catalog/access/1/delete/", "catalog:tool_access_delete", {"pk": 1}, "catalog/tool_access_confirm_delete.html"],
    ]

    @classmethod
    def setUpTestData(cls):
        # Créer plusieurs outils pour les tests de pagination, etc.
        test_user = User.objects.create_user(username="testuser", password="testpassword")

        number_of_tools = 10
        test_tool = AgriculturalTool.objects.create(
            name="Outil test", description="Description test", user=test_user
        )
        for tool_id in range(number_of_tools):
            AgriculturalTool.objects.create(
                name=f"Outil {tool_id}", description=f"Description {tool_id}", user=test_user
            )
        ToolAccess.objects.create(user=test_user, tool = test_tool)

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
        """Test if URL is available with its name"""
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
            start_time_borrow=140,
            end_time_borrow=150.2,
            comment="Test borrow",
        )

        # Test the export URL
        response = self.client.get(reverse("catalog:export_tool", kwargs={"tool_id": 1}))

        # Check if response has the correct status code
        self.assertEqual(response.status_code, 200)

        # Verify the content type is correct for an Excel file
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
