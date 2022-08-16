from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# Q helps handle queries
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # set below as None so are defined if not set in request and therefore empty in context
    query = None
    categories = None
    sort = None
    direction = None

    # check if request.get exists (if get param was sent in request from search form in nav, or when selecting category in nav)
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            # copy sort param into new var called sortkey to preserve value of sort to use later
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                # copy sort param into new var called sortkey to preserve value of sort to use later
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        
        # NAV CATEGORY: 
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # SEARCH BOX: form text input was named q, so check if q is in request.GET
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            # set queries var to Q obj where name or description contains the query, case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # use filter method with queries var passed to it
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        # curent_sorting will be none_none if no sorting selected
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)



















