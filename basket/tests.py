# 3rd Party Imports
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Internal Imports
from products.models import Product, Category
from basket.views import add_to_basket, view_basket


class BasketViewTests(TestCase):
    def setUp(self):
        # Create test data, such as products and categories,
        # to use in the tests
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=9.99
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def tearDown(self):
        # Clean up test data after each test method runs
        self.product.delete()
        self.category.delete()
        self.user.delete()

    def test_view_basket(self):
        # Test the view_basket view
        url = reverse('view_basket')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

    def test_add_to_basket(self):
        # Test the add_to_basket view
        url = reverse('add_to_basket', args=[self.product.id])
        data = {
            'quantity': 2,
            'redirect_url': reverse('view_basket')
        }
        response = self.client.post(url, data)

        # Check if the response redirects to the basket page
        self.assertRedirects(response, reverse('view_basket'))

        # Check if the item was added to the basket
        basket = self.client.session.get('basket', {})
        self.assertTrue(str(self.product.id) in basket)
        self.assertEqual(basket[str(self.product.id)], 2)

    def test_add_to_basket_with_size(self):
        # Test the add_to_basket view with a specified size
        url = reverse('add_to_basket', args=[self.product.id])
        data = {
            'quantity': 1,
            'redirect_url': reverse('view_basket'),
            'product_size': 'medium'  # Specify a size
        }
        response = self.client.post(url, data)

        # Check if the response redirects to the basket page
        self.assertRedirects(response, reverse('view_basket'))

        # Check if the item with size was added to the basket
        basket = self.client.session.get('basket', {})
        self.assertTrue(str(self.product.id) in basket)
        self.assertTrue('items_by_size' in basket[str(self.product.id)])
        self.assertEqual(
            basket[str(self.product.id)]['items_by_size']['medium'],
            1
        )
