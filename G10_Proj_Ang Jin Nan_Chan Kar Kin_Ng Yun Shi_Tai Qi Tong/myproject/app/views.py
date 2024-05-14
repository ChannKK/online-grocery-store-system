from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpRequest
from datetime import datetime
from django.contrib.auth.decorators import login_required
from addproduct.models import Product
from app.models import Feedback
from app.models import Order, OrderItem
from django.db.models import Func, F, Value, Sum, Count
from django.db.models.functions import TruncDate
from viewunassignedorder.models import DeliveryOrder

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
    else:
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'year':datetime.now().year,
        }
    )
    
def report(request):
    assert isinstance(request, HttpRequest)
    check_manager = request.user.groups.filter(name='manager').exists()
    context={
        'title': 'Report',
        'is_manager': check_manager,
        'year':datetime.now().year,
    }
    
    if request.method == 'GET':

        selected_month = request.GET.get('month')
        if selected_month:
            select = True
            selected_year, selected_month_number = selected_month.split('-')

            selected_orders = Order.objects.annotate(
                truncated_date=TruncDate('order_date')
            ).filter(
                truncated_date__year=selected_year,
                truncated_date__month=selected_month_number
            ).values(formatted_date=Func(F('truncated_date'), Value('%Y-%m'), function='strftime'),
                    total_orders=F('order_id'))
            total_orders = selected_orders.count()
            total_earned = selected_orders.aggregate(Sum('order_amt'))['order_amt__sum'] or 0
            top_selling = OrderItem.objects.filter(
                order_id__in=selected_orders.values('order_id')
            ).values('product_id__product_name').annotate(
                product_count=Count('product_id')
            ).order_by('-product_count')

            if top_selling:
                top_quantity = top_selling.first()['product_count']
                
                same_quantity_items = top_selling.filter(product_count=top_quantity)
                
                product_names = [item['product_id__product_name'] for item in same_quantity_items]
                product_counts = [item['product_count'] for item in same_quantity_items]
                
                highest_selling = ", ".join([f"{name}, {count} solds" for name, count in zip(product_names, product_counts)])
            else:
                highest_selling = "-"


            context = {
                'selected_year' : selected_year,
                'selected_month_number' : selected_month_number,
                'total_orders' : total_orders,
                'total_earned' : total_earned,
                'select' : select,
                'highest_selling' : highest_selling,
                'is_manager': check_manager,
                'year':datetime.now().year,
                'title': 'Report',
            }

    return render(request,'app/report.html',context)

def feedback(request):
    assert isinstance(request, HttpRequest)
    check_manager = request.user.groups.filter(name='manager').exists()
    context={
        'title': 'Feedback',
        'is_manager': check_manager,
        'year':datetime.now().year,
    }
    feedbacks = Feedback.objects.all()
    if request.method == 'GET':
        context['feedbacks']=feedbacks
        
    if request.method == 'POST':
        feedback_update = Feedback.objects.get(feedback_id=request.POST['feedback_id'])
        feedback_update.manager = request.user
        feedback_update.feedback_reply = request.POST['feedback_reply']
        feedback_update.save(update_fields=['manager_id', 'feedback_reply'])
        return redirect('feedback')
    
    return render(request,'app/feedback.html',context)
    
def cart(request):
    return render(request,'app/cart.html')

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Online Grocery Store System',
            'message':'About Us',
            'year':datetime.now().year,
        }
    )


@login_required
def menu(request):
    check_store_staff = request.user.groups.filter(name='store staff').exists()
    check_manager = request.user.groups.filter(name='manager').exists()
    check_customer = request.user.groups.filter(name='customer').exists()
    check_delivery_staff = request.user.groups.filter(name='delivery staff').exists()

    if check_store_staff:
        return redirect(reverse('order_view')) 
    
    context = {
        'title': 'Main Menu',
        'is_store_staff': check_store_staff,
        'is_manager': check_manager,
        'is_customer': check_customer,
        'is_delivery_staff': check_delivery_staff,

        'year': datetime.now().year,
    }
    context['user'] = request.user

    if check_manager or check_customer:
        products = Product.objects.all()  
        context['products'] = products
    return render(request, 'app/menu.html', context)

def delete_product(request, product_id):
    if request.method == 'POST':
        if request.user.groups.filter(name='manager').exists():
            try:
                product = Product.objects.get(product_id=product_id)
                product.delete()
                messages.success(request, 'Product deleted successfully.')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found. Please enter a valid Product ID.')
        else:
            messages.error(request, 'You do not have permission to delete products.')
    return redirect('menu')

def view_prod_details(request, productID):
    context = {
        'title': 'Product Information',
        'year': datetime.now().year,
        'user': request.user,
    }

    if request.method == 'GET':
        product = get_object_or_404(Product, productID=productID)
        context['product'] = product

        try:
            productInfo = Product.objects.get(product=product)
            context['productInfo'] = productInfo
        except Product.DoesNotExist:
            context['productInfo'] = None

    return render(request, 'viewproducts/view_prod_details.html', context)

def view_unassigned_orders(request):
    if request.user.groups.filter(name='delivery staff').exists():
        orders = DeliveryOrder.objects.filter(is_assigned=False)  
        return render(request, 'viewunassignedorder/unassigned_orders.html', {'orders': orders})  

    return redirect('menu')

