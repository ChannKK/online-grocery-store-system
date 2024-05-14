from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from addproduct.models import Product
from django.contrib import messages

# Create your views here.

@login_required
def addproductform(request):
    check_manager = request.user.groups.filter(name='manager').exists()
    context = {
    'is_manager': check_manager,
	'title':'Add Product Form',
	'year': datetime.now().year,
	}
    
    context['user'] = request.user
    return render(request,'addproduct/addproductform.html',context)

def update_product(request, product_id):
    check_manager = request.user.groups.filter(name='manager').exists()
    context = {
	'title':'Add Product Form',
    'is_manager': check_manager,
	'year': datetime.now().year,
    }
    context['user'] = request.user
    if request.method == 'GET':
        product = Product.objects.get(product_id=product_id)
        context['product'] = product
         
    if request.method== 'POST':
        product = Product.objects.get(product_id=product_id)
        # product.delete()
        # latest_product_id=product_id
        # latest_product_name = request.POST['product_name']
        # latest_product_price = request.POST['product_price']
        # latest_product_qty = request.POST['product_qty']
        # latest_product_info = request.POST['product_info']
        # product.product_id=product_id
        product.product_name = request.POST['product_name']
        product.product_price = request.POST['product_price']
        product.product_qty = request.POST['product_qty']
        product.product_info = request.POST['product_info']
        
        if 'product_pic' in request.FILES:
            product.product_pic = request.FILES['product_pic']
            
        product.save(update_fields=['product_name','product_price','product_qty','product_info', 'product_pic'] )
        
        # latest_product=Product(
        #     product_id=latest_product_id, 
        #     product_name=latest_product_name, 
        #     product_price=latest_product_price, 
        #     product_qty=latest_product_qty, 
        #     product_info=latest_product_info, 
        #     product_pic=latest_product_pic
        # )
        # latest_product.save()
        # context = {
        #     'product_id': latest_product_id,
        #     'product_name' : latest_product_name,
        #     'product_price' : latest_product_price,
        #     'product_qty' : latest_product_qty,
        #     'product_info' : latest_product_info,
        #     'product_pic' : latest_product_pic
        # }
        messages.success(request, 'Product information updated successfully.')
        return redirect('menu')
    return render(request, 'addproduct/update_product.html', context)

def addproductconfirmation(request):
    check_manager = request.user.groups.filter(name='manager').exists()
    newproduct_id = request.POST['product_id']
    newproduct_name = request.POST['product_name']
    newproduct_price = request.POST['product_price']
    newproduct_qty = request.POST['product_qty']
    newproduct_info = request.POST['product_info']
    newproduct_pic = request.FILES['product_pic']
                
    newproduct = Product(
        product_id=newproduct_id,
        product_name=newproduct_name,
        product_price=newproduct_price,
        product_qty=newproduct_qty,
        product_info=newproduct_info,
        product_pic=newproduct_pic
    )
    newproduct.save()

    context = {
        'title': 'Add Product Confirmation',
        'is_manager': check_manager,
        'product_id': newproduct_id,
        'product_name': newproduct_name,
        'product_price': newproduct_price,
        'product_qty': newproduct_qty,
        'product_info': newproduct_info,
        'product_pic' : newproduct_pic,
    }
    context['products'] = newproduct
    return render(request, 'addproduct/addproductconfirmation.html', context)
