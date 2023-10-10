from django.test import TestCase
from .models import Category, Product


class CategoryModelTest(TestCase):
    """
    Test case for the Category model.
    """

    def test_category_creation(self):
        """
        Test the creation of a Category instance.
        """
        category = Category.objects.create(
            name='Test Category',
            friendly_name='Friendly Test Category'
        )
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.friendly_name, 'Friendly Test Category')


class ProductModelTest(TestCase):
    """
    Test case for the Product model.
    """

    def test_product_creation(self):
        """
        Test the creation of a Product instance.
        """
        category = Category.objects.create(
            name='Test Category'
        )
        product = Product.objects.create(
            code='ABC123',
            brand='Test Brand',
            name='Test Product',
            description='This is a test product.',
            has_sizes=True,
            price=19.99,
            category=category,
            rating=4.5
        )
        self.assertEqual(product.code, 'ABC123')
        self.assertEqual(product.brand, 'Test Brand')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'This is a test product.')
        self.assertTrue(product.has_sizes)
        self.assertAlmostEqual(product.price, 19.99, places=2)
        self.assertEqual(product.category, category)
        self.assertAlmostEqual(product.rating, 4.5, places=2)

