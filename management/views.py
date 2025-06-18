from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.models import Product, Order
import os
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.db.models import Count

class ProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'management/product_list.html'
    context_object_name = 'products'
    
    def test_func(self):
        return self.request.user.groups.filter(name='Store Managers').exists() or self.request.user.is_superuser

def is_manager(user):
    return user.groups.filter(name='Store Managers').exists() or user.is_superuser

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.annotate(
        item_count=Count('orderitem')
    ).filter(
        transaction_id__isnull=False,
        item_count__gt=0
    ).count()
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
    }
    return render(request, 'management/dashboard.html', context)  

@login_required
@user_passes_test(is_manager)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category', '')  
        image = request.FILES.get('image')
        
        product = Product.objects.create(
            name=name,
            price=price,
            category=category,  
            image=image
        )
        
        messages.success(request, 'Prodotto aggiunto con successo!')
        return redirect('management:product_list')
        
    context = {
        'title': 'Aggiungi Prodotto'
    }
    return render(request, 'management/product_form.html', context)

@login_required
@user_passes_test(is_manager)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.category = request.POST.get('category', '')  
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        messages.success(request, 'Prodotto modificato con successo!')
        return redirect('management:product_list')
        
    context = {
        'title': 'Modifica Prodotto',
        'product': product
    }
    return render(request, 'management/product_form.html', context)

@login_required
@user_passes_test(is_manager)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Prodotto eliminato con successo!')
        return redirect('management:product_list')
    
    return render(request, 'management/product_confirm_delete.html', {
        'product': product
    })

@login_required
@user_passes_test(is_manager)
def order_list(request):
    orders = Order.objects.annotate(
        item_count=Count('orderitem')
    ).filter(
        transaction_id__isnull=False,
        item_count__gt=0
    ).order_by('-date_ordered')
    context = {
        'orders': orders,
        'title': 'Orders List'
    }
    return render(request, 'management/order_list.html', context)

@login_required
@user_passes_test(is_manager)
def mark_order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.complete = True
        order.save()
        messages.success(request, f'Order #{order.id} has been marked as complete!')
    return redirect('management:order_list')

@login_required
@user_passes_test(is_manager)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer
    other_orders = Order.objects.annotate(
        item_count=Count('orderitem')
    ).filter(
        customer=customer,
        transaction_id__isnull=False,
        item_count__gt=0
    ).exclude(id=order_id).order_by('-date_ordered')
    
    context = {
        'order': order,
        'other_orders': other_orders,
        'customer': customer
    }
    return render(request, 'management/order_detail.html', context)
