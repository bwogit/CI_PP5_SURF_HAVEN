from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
# Internal
from products.models import Product


def basket_contents(request):

    basket_items = []
    product_count = 0
    total = 0

    basket = request.session.get('basket', {})

    for item_id, quantity_data in basket.items():
        # Check if 'quantity' is a dictionary
        if isinstance(quantity_data, dict):
            # Extract the numeric value from the 'quantity' dictionary
            quantity = quantity_data.get('value', 0)  # Replace 'value' with the correct key
        else:
            # If 'quantity' is not a dictionary, assume it's a numeric value
            quantity = quantity_data

    try:
        product = Product.objects.get(pk=item_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")

    item_total = quantity * product.price
    total += item_total
    product_count += quantity

    basket_item = {
        'item_id': item_id,
        'quantity': quantity,
        'product': product,
        'item_total': item_total,
    }
    basket_items.append(basket_item)

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
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                basket_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

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
