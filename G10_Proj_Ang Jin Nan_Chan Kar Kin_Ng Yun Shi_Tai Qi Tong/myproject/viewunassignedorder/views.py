from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DeliveryOrder
from app.models import Order
from app.forms import ProofOfDeliveryForm
from django.contrib import messages
import os
from django.http import HttpResponseBadRequest

@login_required
def view_unassigned_orders(request):
    unassigned_orders = Order.objects.filter(order_status='Ready for Delivery')
    return render(request, 'viewunassignedorder/unassigned_orders.html', {'orders': unassigned_orders})

def accept_order(request, order_id): 
    order = get_object_or_404(DeliveryOrder, order_id=order_id)
    order.delivery_status = 'Accepted'
    order.save()
    return redirect('view_assigned_orders')

def decline_order(request, order_id):
    order = get_object_or_404(DeliveryOrder, order_id=order_id)
    order.delivery_status = 'Declined' 
    order.save()
    return redirect('view_unassigned_orders')

def view_assigned_orders(request):
    assigned_orders = DeliveryOrder.objects.filter(delivery_status='Accepted')
    return render(request, 'viewunassignedorder/view_assigned_orders.html', {'orders': assigned_orders})


def confirm_order(request):
    if request.method == 'POST':
        selected_delivery_id = request.POST.get('delivery_id')
        new_delivery_status = request.POST.get('delivery_status')
        try:
            delivery_orders = DeliveryOrder.objects.filter(delivery_id=selected_delivery_id)
            if delivery_orders.exists():
                for delivery_order in delivery_orders:
                    delivery_order.delivery_status = new_delivery_status
                    delivery_order.save()

                if new_delivery_status == 'Completed':
                    messages.success(request, 'Delivery status updated successfully.')
                return redirect('view_assigned_orders')
            else:
                messages.error(request, 'Invalid delivery ID.')
                return redirect('confirm_order')
        except DeliveryOrder.DoesNotExist:
            messages.error(request, 'Invalid delivery ID.')
            return redirect('confirm_order')
    else:
        assigned_orders = DeliveryOrder.objects.filter(delivery_status='Accepted')
        delivery_ids = [order.delivery_id for order in assigned_orders]
        form = ProofOfDeliveryForm()

    return render(request, 'viewunassignedorder/confirm_order.html', {'form': form, 'delivery_ids': delivery_ids})