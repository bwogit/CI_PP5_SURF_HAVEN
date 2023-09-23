from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('basket', {})
    if not bag:
        messages.error(request, "Your basket is empty")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51NnHHMLbIUmMAFawKvDMt83PYXeKuImne9vCybtmhR0V5XohETQEG5ueLEYIUH8V3XRHcciuqcgui7IVHaogQHVg00CiqB4EZI',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
