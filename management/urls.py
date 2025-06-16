from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.ProductListView.as_view(), name='product_list'),  
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/complete/', views.mark_order_complete, name='mark_order_complete'),
]