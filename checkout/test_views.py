# 3rd party Imports
from django.test import TestCase
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
# Internal imports:
from checkout.models import Order
from profiles.models import UserProfile


class TestCheckout(TestCase):
    """
    A class for testing the checkout app views
    """
    def setUp(self):
        """
        Create test users, regular, and superuser and a test order
        """
        test_user = User.objects.create_user(
            username='testuser1', password='testpassword1')
        test_user_superuser = User.objects.create_superuser(
            username='testsuperuser', password='testpassword')

        test_user.save()
        test_user_superuser.save()
        test_user = UserProfile.objects.get(user=test_user)

        Order.objects.create(
            full_name='Test Name',
            email='testuser@gmail.com',
            phone_number='123456789',
            address1='Test Address1',
            address2='Test Address2',
            county='test_county',
            country='test_country',
            town_or_city='Test_city',
        )

    def reset(self):
        """
        Delete test orders
        """
        Order.objects.all().delete()

    def test_checkout_view_empty_cart(self):
        """
        This tests an empty basket 
        """
        response = self.client.get('/checkout/')
        self.assertRedirects(response, '/products/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Your basket is empty")
