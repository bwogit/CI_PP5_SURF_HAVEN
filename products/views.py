# 3rd Party
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Internal
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, sorting and search queries """

    products = Product.objects.all()
    categories_list = Category.objects.all()
    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please input search criteria")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | \
                Q(description__icontains=query)
            products = products.filter(queries)

    current_sort = f'{sort}_{direction}'

    context = {
        'products': products,
        'categories_list': categories_list,
        'search_term': query,
        'current_sort': current_sort
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    """ A view to show selected product details """

    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()

    context = {
        'product': product,
        'categories': categories,
        'categories_list': Category.objects.all(),
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    Add a product to the shop
    """

    categories_list = Category.objects.all()

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admins can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product to shop.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please check form is valid.'
                )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'categories_list': categories_list,
    }

    return render(request, template, context)
