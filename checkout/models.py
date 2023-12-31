# Standard library imports
import uuid
# Django imports
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField
from profiles.models import UserProfile
from products.models import Product


class Order(models.Model):
    """
    A Django model representing an order placed by a customer.
    """
    order_number = models.CharField(max_length=35,
                                    null=False, editable=False, default='')
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
        )
    full_name = models.CharField(max_length=55,
                                 null=False, blank=False, default='')
    email = models.EmailField(max_length=254,
                              null=False, blank=False, default='')
    phone_number = models.CharField(max_length=20,
                                    null=False, blank=False, default='')
    town_or_city = models.CharField(max_length=40,
                                    null=False, blank=False, default='')
    address1 = models.CharField(max_length=85,
                                null=False, blank=False, default='')
    address2 = models.CharField(max_length=85,
                                null=True, blank=True, default='')
    county = models.CharField(max_length=80,
                              null=True, blank=True, default='')
    postcode = models.CharField(max_length=20,
                                null=True, blank=True, default='')
    country = CountryField(blank_label='Country *',
                           null=False, blank=False,)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6,
                                        decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254,
                                  null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Recalculate the grand total whenever a line item is added,
        taking into account any associated delivery costs.
        """
        aggregate_result = self.lineitems.aggregate(Sum('lineitem_total'))
        self.order_total = aggregate_result['lineitem_total__sum'] or 0
        ['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total *\
                 settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    A Django model representing a single item on an order.
    """

    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False,
                                blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2,
                                    null=True, blank=True)  # sizes
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Ovveride the default save method to establish
        the line item total and refresh the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'code {self.product.code} on order {self.order.order_number}'
