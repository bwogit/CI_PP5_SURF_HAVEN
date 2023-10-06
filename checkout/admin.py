# Local imports
from .models import Order, OrderLineItem
# 3rd party imports
from django.contrib import admin
# Internal imports
from django.contrib import admin


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Admin inline class for the OrderLineItem model.

    This class allows OrderLineItems to be edited inline within OrderAdmin.
    """

    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for the Order model.

    This class allows Orders to be edited in the Django admin interface.
    """

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'user_profile', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_basket',
                       'stripe_pid',)

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'address1',
              'address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_basket',
              'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)


# Register the Order model with the Django admin interface
admin.site.register(Order, OrderAdmin)