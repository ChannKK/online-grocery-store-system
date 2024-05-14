from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from addproduct.models import Product
from django.db.models import Q

# Create your views here.
@login_required
def sstf_view_products(request):
    title = 'View Products' 
    products = Product.objects.all()
    search_query = request.GET.get('search')
    selected_products = None
    no_results_message = None

    if search_query and search_query.lower() is not None:
        selected_products = Product.objects.filter(Q(product_id__icontains=search_query) | Q(product_name__icontains=search_query))
        if not selected_products.exists():
            no_results_message = 'No products found.'

    context = {'products': selected_products or products, 'search_query': search_query, 'no_results_message': no_results_message, 'title': title, 'year':datetime.now().year}
    return render(request, 'sstf_viewprod/sstf_viewprod.html', context)

def sstf_view_prod_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    title = f'Product Detail - {product.product_name}'
    context = {'selected_product': product, 'title':title, 'year':datetime.now().year}
    return render(request, 'sstf_viewprod/sstf_viewproddetail.html', context)
