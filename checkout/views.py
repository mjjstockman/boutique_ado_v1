from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    # get bag in sesh
    bag = request.session.get('bag', {})
    # error msg if no bag in sesh
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51LYvuADEsL3QJnnRm4jb2tQvHgIAE7hvdqd9ZqrJoydkI9edvSIhgo7jvm9uCKZpnZRx4WtAP4sbxfjmU6pdSnTL00sabpg8HF',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)