# Imports
# 3rd Party
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from products.models import Product

# Internal
from products.models import Product, Category


def view_basket(request):
    """
    A view to display the basket page
    """
    products = Product.objects.all()
    categories_list = Category.objects.all()

    context = {
        'products': products,
        'categories_list': categories_list
               }
    return render(request, 'basket/basket.html', context)


def add_to_basket(request, item_id):
    """ Add a quantity of the product to the basket """
    
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    
    basket = request.session.get('basket', {})
    
    if size:
        if item_id in basket:
            if size in basket[item_id]['items_by_size']:
                basket[item_id]['items_by_size'][size] += quantity
            else:
                basket[item_id]['items_by_size'][size] = quantity
        else:
            basket[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in basket:
            basket[item_id] += quantity
        else:
            basket[item_id] = quantity
            messages.success(request, f'Added {product.name} to your basket')
    
    request.session['basket'] = basket
    return redirect(redirect_url)


def update_basket(request, item_id):

    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    basket = request.session.get('basket', {})

    if size:
        if quantity > 0:
            basket[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {basket[item_id]["items_by_size"][size]}')
        else:
            del basket[item_id]['items_by_size'][size]
            if not basket[item_id]['items_by_size']:
                basket.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your basket')
    else:
        if quantity > 0:
            basket[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {basket[item_id]}')
        else:
            basket.pop(item_id)
            messages.success(request, f'Removed {product.name} from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id):
    """Remove the item from the shopping basket"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        basket = request.session.get('basket', {})

        if size:
            del basket[item_id]['items_by_size'][size]
            if not basket[item_id]['items_by_size']:
                basket.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your basket')
        else:
            basket.pop(item_id)
            messages.success(request, f'Removed {product.name} from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
