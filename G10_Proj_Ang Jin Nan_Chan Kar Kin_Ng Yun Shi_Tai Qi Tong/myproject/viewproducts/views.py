from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from addproduct.models import Product
from viewproducts.models import Cart, CartItem
from django.contrib.auth.models import User
from datetime import datetime
from django.http import JsonResponse
from .cart import Cart
import json

# Create your views here.
@login_required
def view_products(request):
    products = Product.objects.all()
    return render(request, 'addproduct/view_products.html', {'products': products})

def view_prod_details(request, product_id):
    context = {
        'title': 'Product Information',
        'year': datetime.now().year,
        'user': request.user,
    }

    if request.method == 'GET':
        product = get_object_or_404(Product, product_id=product_id)
        context['product'] = product

        context['product_info'] = {
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_info': product.product_info,
                # Add any other fields you want to include
            }
    return render(request, 'viewproducts/view_prod_details.html', context)

def cust_search_prod(request): 
    if request.method == 'GET':
        query = request.GET.get('query')
        print(f"Search Query: {query}")  # Add this line for debugging
        if query:
            products = Product.objects.filter(product_name__icontains=query)
            print(f"Matching Products: {products}")  # Add this line for debugging
            return render(request, 'viewproducts/cust_search_prod.html', {'products': products})
        else:
            print("No product is found")
            return render(request, 'viewproducts/cust_search_prod.html', {})

def cart_summary(request):
    cart = Cart(request)
    cart_items = cart.get_prods()
    cartItem_qty = cart.get_quants()
    cart_amt = cart.cart_total()
    cartItem_subtotal = cart.cartItem_subtotal()  
    
    context = {
        'cart_items': cart_items,
        'cartItem_qty': cartItem_qty,
        'cart_amt': cart_amt,
        'cartItem_subtotal': cartItem_subtotal, 
    }

    return render(request, "viewproducts/cart_summary.html", context)

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        cartItem_qty = int(request.POST.get('cartItem_qty'))
        
        product = get_object_or_404(Product, product_id=product_id)

        # Assuming have a Cart class with an 'add' method
        cart = Cart(request)
        cart.add(product=product, quantity=cartItem_qty)

        print("Cart contents:", cart.cart)
        
        #get cart_qty
        cart_qty = cart.__len__()
        
        # response = JsonResponse({'Product Name': product.product_name})
        response = JsonResponse({'qty': cart_qty})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        cart.delete(product=product_id)
        
        response = JsonResponse({'product': product_id})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        cartItem_qty = int(request.POST.get('cartItem_qty'))
        
        cart.update(product_id, quantity=cartItem_qty)  # Update this line
        
        response = JsonResponse({'qty': cartItem_qty})
        return response

def checkout(request): 
    cart = Cart(request)
    cart_items = cart.get_prods()
    cartItem_qty = cart.get_quants()
    cart_amt = cart.cart_total()
    cartItem_subtotal = cart.cartItem_subtotal()
    user = User(request)

    context = {
        'cart_items': cart_items,
        'cartItem_qty': cartItem_qty,
        'cart_amt': cart_amt,
        'cartItem_subtotal': cartItem_subtotal, 
    }
    
    return render(request, 'viewproducts/checkout.html', context)
    
def order_status(request): 
    return render(request, 'viewproducts/order_status.html')

def completed_order(request):
    return render(request, 'viewproducts/completed_order.html')