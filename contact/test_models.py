# 3rd Party imports:
from django.test import TestCase
from django.contrib.auth.models import User
from phonenumber_field.phonenumber import PhoneNumber
from .models import Contact


class ContactModelTest(TestCase):
    def setUp(self):
        """
        Set up a test user for the Contact model test.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_contact_model_creation(self):
        """
        Test the creation and retrieval of a Contact instance.
        """
        # Create a Contact instance
        contact = Contact.objects.create(
            user=self.user,
            name='John Doe',
            email='johndoe@example.com',
            phone=PhoneNumber.from_string('+1234567890'),
            message='This is a test message.'
        )

        # Retrieve the created Contact object from the database
        saved_contact = Contact.objects.get(pk=contact.pk)

        # Check if the attributes match what was saved
        self.assertEqual(saved_contact.user, self.user)
        self.assertEqual(saved_contact.name, 'John Doe')
        self.assertEqual(saved_contact.email, 'johndoe@example.com')
        self.assertEqual(saved_contact.phone,
                         PhoneNumber.from_string('+1234567890'))
        self.assertEqual(saved_contact.message, 'This is a test message.')
