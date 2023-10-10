from django.test import TestCase
from .forms import OrderForm


class TestOrderForm(TestCase):
    def test_order_form_valid(self):
        """
        Test the OrderForm with valid data.
        """
        form_data = {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'address1': '123 Main St',
            'town_or_city': 'Cityville',
            'country': 'US',
        }

        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid(self):
        """
        Test the OrderForm with invalid data.
        """
        form_data = {
            'full_name': 'Etienne Cabri',  
            'email': 'gg@gmail.m',
            'phone_number': '12345', 
        }

        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
