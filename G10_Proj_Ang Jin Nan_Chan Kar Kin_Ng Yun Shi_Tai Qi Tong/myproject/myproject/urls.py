"""myproject URL Configuration

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app import views as main_views
from addproduct import views as addproduct_views
from sstf_viewprod import views as sstf_viewprod_views
from sstf_checkorder import views as sstf_checkorder_views
from django.conf.urls.static import static
from django.conf import settings
from viewproducts import views as viewproducts_views
import django.contrib.auth.views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from viewunassignedorder import views 
admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', main_views.home, name='home'),
    re_path(r'^contact$', main_views.contact, name='contact'),
    re_path(r'^feedback$', main_views.feedback, name='feedback'),
    re_path(r'^cart$', main_views.cart, name='cart'),
    re_path(r'^report$', main_views.report, name='report'),
    re_path(r'^about$', main_views.about, name='about'),
    re_path(r'^menu$', main_views.menu, name='menu'),
    re_path(r'^addproductform$', addproduct_views.addproductform, name='addproduct_form'),
    re_path(r'^addproductconfirmation$', addproduct_views.addproductconfirmation, name='addproduct_confirmation'),
    re_path(r'^sstf_viewprod$', sstf_viewprod_views.sstf_view_products, name='sstf_viewprod'),
    path('update_product/<str:product_id>/', addproduct_views.update_product, name='update_product'),
    path('deleteproduct/<str:product_id>/', main_views.delete_product, name='deleteproduct'),
    path('update_order_status/<str:order_id>/', sstf_checkorder_views.update_order_status, name='update_order_status'),
    path('sstf_checkorder/', sstf_checkorder_views.order_view, name='order_view'),
    path('sstf_checkorderitem/<str:order_id>/', sstf_checkorder_views.order_items_view, name='order_items_view'),
    path('sstf_viewproddetail/<str:product_id>/', sstf_viewprod_views.sstf_view_prod_detail, name='sstf_viewproddetail'),
    path('view_prod_details/<str:product_id>/', viewproducts_views.view_prod_details, name='view_prod_details'),
    path('cust_search_prod/', viewproducts_views.cust_search_prod, name='cust_search_prod'),
    path('cart/', viewproducts_views.cart_summary, name='cart_summary'),
    path('cart_add/', viewproducts_views.cart_add, name='cart_add'),
    path('cart_delete/', viewproducts_views.cart_delete, name="cart_delete"),
    path('cart_update/', viewproducts_views.cart_update, name="cart_update"),
    path('checkout/', viewproducts_views.checkout, name="checkout"),
    path('completed_order/', viewproducts_views.completed_order, name="completed_order"),
    path('order_status/', viewproducts_views.order_status, name="order_status"),
    
    re_path(r'^login/$', LoginView.as_view(template_name = 'app/login.html'), name='login'),
    re_path(r'^logout$', LogoutView.as_view(template_name = 'app/index.html'), name='logout'),

    path('unassigned_orders/', views.view_unassigned_orders, name='view_unassigned_orders'),
    path('accept_order/<str:order_id>/', views.accept_order, name='accept_order'),
    path('decline_order/<str:order_id>/', views.decline_order, name='decline_order'),
    path('view_assigned_orders/', views.view_assigned_orders, name='view_assigned_orders'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    #path('complete_order/<str:order_id>/', views.complete_order, name='complete_order'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)