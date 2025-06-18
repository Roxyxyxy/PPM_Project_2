from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import json
import datetime
import traceback
from .models import *

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.error(request, "Username o password non validi.")
        else:
            messages.error(request, "Username o password non validi.")
    else:
        form = AuthenticationForm()
    
    # Calcola cartItems come nelle altre viste
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except:
            cart = {}
        cartItems = 0
        for i in cart:
            try:
                cartItems += cart[i]['quantity']
            except:
                pass
    
    return render(request, 'registration/login.html', {
        'form': form, 
        'cartItems': cartItems
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Crea il customer associato
            Customer.objects.get_or_create(
                user=user,
                defaults={'name': user.username}
            )
            
            # Login automatico
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Account creato con successo per {username}!')
                return redirect('store')
            else:
                messages.error(request, 'Errore durante il login automatico')
    else:
        form = UserCreationForm()
    
    # Gestione conteggio carrello
    cartItems = 0
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
            if order:
                cartItems = order.get_cart_items
        except:
            pass
    
    return render(request, 'registration/register.html', {'form': form, 'cartItems': cartItems})

def store(request):
    category = request.GET.get('category')
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user, name=request.user.username)
        
        order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0
        
        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                
                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)
                
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass

    context = {
        'products': products,
        'cartItems': cartItems,
        'category': category
    }
    
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user, name=request.user.username)
            
        order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0
        
        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                
                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)
                
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user, name=request.user.username)
            
        order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.warning(request, "Devi accedere per completare l'acquisto.")
        return redirect('login')

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def processOrder(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'È necessario effettuare il login per completare l\'ordine'}, status=403)

        data = json.loads(request.body)
        
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user, name=request.user.username)

        order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
        
        if order.get_cart_items <= 0:
            return JsonResponse({'error': 'Il carrello è vuoto'}, status=400)

        total_from_form = float(data['form'].get('total', 0))
        cart_total = float(order.get_cart_total)

        if total_from_form != cart_total:
            return JsonResponse({'error': 'Il totale non corrisponde'}, status=400)

        # L'ordine viene finalizzato con un ID transazione ma resta 'complete=False'.
        # Sarà l'admin a marcarlo come completato.
        order.transaction_id = datetime.datetime.now().timestamp()
        order.save()

        try:
            if order.shipping:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    name=data['shipping']['name'],
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )
        except Exception as e:
            print(f"Errore durante il salvataggio dell'indirizzo di spedizione: {e}")
            return JsonResponse({'error': 'Errore nel salvataggio dell\'indirizzo di spedizione'}, status=400)
        
        return JsonResponse('Pagamento inviato con successo', safe=False)

    except Exception as e:
        print(f"Errore durante l'elaborazione dell'ordine: {e}")
        traceback.print_exc()
        return JsonResponse({'error': 'Errore durante l\'elaborazione dell\'ordine'}, status=400)
    
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def logout_view(request):
    logout(request)
    response = redirect('login')
    # Opzionale: Eliminare il cookie del carrello
    if 'cart' in request.COOKIES:
        response.delete_cookie('cart')
    return response

def my_orders(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Devi accedere per visualizzare i tuoi ordini.")
        return redirect('login')
        
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user, name=request.user.username)
        
    # Recupera tutti gli ordini inviati (sia completati che in attesa)
    orders = Order.objects.filter(customer=customer, transaction_id__isnull=False).order_by('-date_ordered')
    
    # Calcolo cartItems per il carrello corrente (senza transaction_id)
    try:
        current_order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=None)
        cartItems = current_order.get_cart_items if current_order else 0
    except:
        cartItems = 0
    
    context = {
        'orders': orders,
        'cartItems': cartItems,
        'just_completed': 'refresh' in request.GET
    }
    return render(request, 'store/my_orders.html', context)