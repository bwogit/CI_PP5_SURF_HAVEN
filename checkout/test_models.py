# 3rd PArty Imports
from decimal import Decimal, ROUND_DOWN
from django.test import TestCase
from django.conf import settings
# Internal Imports
from .models import Order, OrderLineItem
from products.models import Product


class TestCheckoutModels(TestCase):
    """
    A class for testing checkout models
    """
    def test_update_total(self):
        # Create an order
        order = Order.objects.create(
            full_name='Test Name',
            email='test@gmail.com',
            phone_number='123456789',
            address1='Test Address',
            address2='Test Address2',
            county='Kildare',
            country='Ireland',
            town_or_city='Test City',
        )

        # Create a product
        product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
            # Add other required fields here
        )

        # Create an order line item with a quantity of 2
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2,
        )

        # Calculate the expected delivery cost and grand total
        total = order_line_item.product.price * order_line_item.quantity
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        expected_grand_total = total + delivery

        # Call the update_total method to calculate the new grand total
        order.update_total()

        # Round both values to 2 decimal places for comparison
        expected_grand_total = expected_grand_total.quantize(
            Decimal('0.00'), rounding=ROUND_DOWN)
        actual_grand_total = order.grand_total.quantize(
            Decimal('0.00'), rounding=ROUND_DOWN)

        # Check if the rounded grand total matches the expected value
        self.assertEqual(actual_grand_total, expected_grand_total)
