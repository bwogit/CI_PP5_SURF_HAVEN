# 3rd Party Imports
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, Http404

# Internal Imports
from products.models import Product


def basket_contents(request):
    """
    Retrieve and process the contents of the shopping basket.
    """
    basket_items = []
    product_count = 0
    total = 0

    basket = request.session.get('basket', {})

    for item_id, item_data in basket.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            basket_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            product_added = False

            for size, quantity in item_data['items_by_size'].items():
                if not product_added:
                    basket_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'size': size,
                    })
                    product_added = True
                else:
                    for item in basket_items:
                        if item['item_id'] == item_id\
                             and item.get('size') == size:
                            item['quantity'] += quantity

            if product_added:
                total += sum(quantity for size,
                             quantity in item_data['items_by_size'].items()) *\
                              product.price

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = total + delivery

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
