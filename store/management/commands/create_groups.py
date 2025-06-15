from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Order

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **options):
        # Create manager group
        manager_group, created = Group.objects.get_or_create(name='Store Managers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Store Managers group'))
        
        # Create customer group
        customer_group, created = Group.objects.get_or_create(name='Customers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Customers group'))
        
        # Get content types
        product_ct = ContentType.objects.get_for_model(Product)
        order_ct = ContentType.objects.get_for_model(Order)
        
        # Manager permissions (full access)
        product_permissions = Permission.objects.filter(content_type=product_ct)
        order_permissions = Permission.objects.filter(content_type=order_ct)
        
        # Customer permissions (read-only for products, create/read for orders)
        customer_product_permissions = Permission.objects.filter(
            content_type=product_ct,
            codename__startswith='view_'
        )
        customer_order_permissions = Permission.objects.filter(
            content_type=order_ct,
            codename__in=['add_order', 'view_order', 'change_order']
        )
        
        # Add permissions to manager group
        manager_group.permissions.add(*product_permissions)
        manager_group.permissions.add(*order_permissions)
        
        # Add permissions to customer group
        customer_group.permissions.add(*customer_product_permissions)
        customer_group.permissions.add(*customer_order_permissions)
        
        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions to both groups'))