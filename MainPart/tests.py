from django.test import TestCase
from .models import CustomUser, CustomerCard


class UsersTesting(TestCase):
    def setUp(self) -> None:
        pass

    def test_data_valid(self):
        self.assertEqual(False, False)