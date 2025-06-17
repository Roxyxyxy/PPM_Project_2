from django.shortcuts import render
from django.http import JsonResponse
from .models import * 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import json
import datetime

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
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
            # Salva l'utente
            user = form.save()
            
            # Crea il customer associato
            Customer.objects.get_or_create(
                user=user,
                defaults={'name': user.username}
            )
            
            # Login automatico - modo più affidabile
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Aggiungi un messaggio per debug
                messages.success(request, f'Benvenuto {username}!')
                return redirect('store')
            else:
                messages.error(request, 'Errore durante il login automatico')
        
        # Se arriviamo qui, c'è stato un errore nel form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Errore in {field}: {error}")
    else:
        form = UserCreationForm()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
    
    return render(request, 'registration/register.html', {'form': form, 'cartItems': cartItems})

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    try:
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == float(order.get_cart_total):
                order.complete = True
            order.save()

            if order.shipping == True and 'shipping' in data:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )
        else:
            print('User is not logged in')
            name = data['form']['name']
            
            # Crea un cliente guest
            customer = Customer.objects.create(
                name=name
            )
            
            # Crea un ordine
            order = Order.objects.create(
                customer=customer,
                complete=False, 
                transaction_id=transaction_id
            )
            
            # Processa il carrello
            try:
                cart = json.loads(request.COOKIES.get('cart', '{}'))
                for item_id in cart:
                    product = Product.objects.get(id=item_id)
                    quantity = cart[item_id]['quantity']
                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=quantity
                    )
            except Exception as e:
                print(f"Error processing cart: {e}")
            
            # Salva indirizzo, solo se presente
            if 'shipping' in data:
                try:
                    ShippingAddress.objects.create(
                        customer=customer,
                        order=order,
                        address=data['shipping']['address'],
                        city=data['shipping']['city'],
                        state=data['shipping']['state'],
                        zipcode=data['shipping']['zipcode'],
                    )
                except Exception as e:
                    print(f"Error saving shipping address: {e}")

        # Prepara risposta
        response = JsonResponse('Payment submitted..', safe=False)
        
        # Svuota carrello
        if not request.user.is_authenticated:
            response.set_cookie('cart', '{}', max_age=86400)
        
        return response
    
    except Exception as e:
        print(f"Order processing error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse('Error processing order', safe=False, status=200)  # Cambio a 200 per evitare errori in frontend

def logout_view(request):
    logout(request)
    response = redirect('login')
    # Opzionale: Eliminare il cookie del carrello
    if 'cart' in request.COOKIES:
        response.delete_cookie('cart')
    return response