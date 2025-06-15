from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from store.models import Product, Order
import os

def is_manager(user):
    return user.groups.filter(name='Store Managers').exists() or user.is_superuser

@login_required
@user_passes_test(is_manager)
def dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(complete=False).count()
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'management/dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'management/product_list.html', {'products': products})

@login_required
@user_passes_test(is_manager)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        digital = 'digital' in request.POST
        image = request.FILES.get('image')
        
        product = Product(name=name, price=price, digital=digital)
        if image:
            product.image = image
        product.save()
        
        messages.success(request, 'Prodotto aggiunto con successo!')
        return redirect('management:product_list')
    
    return render(request, 'management/product_form.html', {'title': 'Aggiungi Prodotto'})

@login_required
@user_passes_test(is_manager)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.digital = 'digital' in request.POST
        
        image = request.FILES.get('image')
        if image:
            # Puoi aggiungere qui la logica per eliminare l'immagine esistente
            product.image = image
        
        product.save()
        messages.success(request, 'Prodotto modificato con successo!')
        return redirect('management:product_list')
    
    return render(request, 'management/product_form.html', {
        'title': 'Modifica Prodotto',
        'product': product
    })

@login_required
@user_passes_test(is_manager)
def delete_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product_name = product.name
        
        # Puoi aggiungere qui la logica per eliminare l'immagine
        
        product.delete()
        messages.success(request, f'Prodotto "{product_name}" eliminato con successo!')
    
    return redirect('management:product_list')