from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from app.models import Order, OrderItem
from django.contrib.auth.models import User

@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        try:
            order = Order.objects.get(order_id=order_id)

            if request.user.username == order.staff.username:
                order.order_status = new_status
                order.save()
                messages.success(request, 'Order status updated successfully.')
            else:
                messages.error(request, 'You do not have permission to update the order status.')

        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')

    return redirect('order_view')

def order_view(request):
    title = 'View Orders' 
    year = datetime.now().year

    if 'search' in request.GET and request.GET['search']:
        search_query = request.GET['search']

        # Check if the customer exists
        if not User.objects.filter(username=search_query).exists():
            messages.error(request, f'Customer with ID "{search_query}" does not exist.')
            orders = Order.objects.none()
        else:
            # Check if orders exist for the specified customer ID
            orders = Order.objects.filter(customer__username=search_query)

            # Order status filter
            order_status_filter = request.GET.get('order_status')
            if order_status_filter:
                orders = orders.filter(order_status=order_status_filter)

            if not orders.exists():
                messages.error(request, f'Customer with ID "{search_query}" has no orders.')
                orders = Order.objects.none()
    else:
        # Order status filter
        order_status_filter = request.GET.get('order_status')
        if order_status_filter:
            orders = Order.objects.filter(order_status=order_status_filter)
        else:
            orders = Order.objects.all().order_by('-order_date') 

    context = {
        'year' : year,
        'orders' : orders,
        'title' : title,
    }

    return render(request, 'sstf_checkorder/sstf_checkorder.html', context)


def order_items_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    title = f'Order Detail - {order.order_id}'
    year = datetime.now().year

    context = {
        'order': order,
        'order_items': order_items,
        'title':title,
        'year':year,
    }

    return render(request, 'sstf_checkorder/sstf_vieworderdetail.html', context)