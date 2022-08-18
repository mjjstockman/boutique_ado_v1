from django.shortcuts import render, redirect

# Create your views here.
def view_bag(request):
    """ A view to return the bag contents page
    """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    # if size is in request URL set it to the value
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})

    # if item has a size...
    if size:
        # ...and item_id is already in bag...
        if item_id in list(bag.keys()):
            # ...and it has the same size as user is now adding...
            if size in bag[item_id]['items_by_size'].keys():
                # ...update quantity
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # ...if same item but diff size, add item_id and size to bag
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # if item not already in bag add it as a dict so can include size
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # if item doesn't have a size, update quantity / add item and quantity
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag

    return redirect(redirect_url)