from django.urls import path

from . import views

urlpatterns = [
    # URL esistenti
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('accounts/register/', views.register_view, name='register'),
]