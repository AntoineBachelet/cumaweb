"""Definition of unit tests of catalog application"""

from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import AgriculturalTool


class AgriculturalToolModelTest(TestCase):
    """Unit tests for the model of AgriculturalTool"""

    @classmethod
    def setUpTestData(cls):
        # Create user for tests
        test_user = User.objects.create_user(username="testuser", password="testpassword")

        # Create tools for tests
        AgriculturalTool.objects.create(
            name="Tracteur de test",
            description="Un tracteur pour les tests unitaires",
            user=test_user,
        )

    def test_tool_name_max_length(self):
        """Test if tool name got the right max length"""
        tool = AgriculturalTool.objects.get(id=1)
        max_length = tool._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)
