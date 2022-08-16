from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# Q helps handle queries
from django.db.models import Q
from .models import Product, Category


# Create your views here.
def all_products(request):
    """ A view to show all products, including sorting and search queries
    """

    products = Product.objects.all()
    # set query as None so no error when adding empty query to context
    query = None
    categories = None

    # check if request.get exists (if get param was sent in request from search form in nav, or when selecting category in nav)
    if request.GET:
        # NAV CATEGORY: 
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            # double underscore as looking for name field of category model (related via FK)
            products = products.filter(category__name__in=categories)
            # change categories str from url into categories obj so can access its fields in template
            categories = Category.objects.filter(name__in=categories)
        # SEARCH BOX: form text input was named q, so check if q is in request.GET
        if 'q' in request.GET:
            # if so rename q as query var
            query = request.GET['q']
            # if search box was blank q will not be in request.GET
            if not query:
                # use django messages framework to add error msg to request
                messages.error(request, "You didn't enter any search criteria!")
                # redirect to products url
                return redirect(reverse('products'))

            # set queries var to Q obj where name or description contains the query, case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # use filter method with queries var passed to it
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details
    """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
