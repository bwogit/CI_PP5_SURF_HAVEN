from django.test import TestCase
from .forms import ContactForm

class ContactFormTest(TestCase):
    def test_valid_email(self):
        """
        Test that a valid email address is accepted.
        """
        form_data = {
            'email': 'valid@example.com',
            'name': 'John Doe',
            'message': 'Hello, this is a test message.',
            'phone': '+353123456789',
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """
        Test that an invalid email address is rejected.
        """
        form_data = {
            'email': 'invalid_email',
            'name': 'Jane Smith',
            'message': 'Another test message.',
            'phone': '+353987654321',
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
