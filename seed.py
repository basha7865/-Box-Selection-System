import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recommender.models import Product, ShippingBox

# Clear existing data
Product.objects.all().delete()
ShippingBox.objects.all().delete()

# Create Sample Products
Product.objects.create(name="Hardcover Book", length=20, width=15, height=3, weight=0.6)
Product.objects.create(name="Wireless Keyboard", length=44, width=13, height=3, weight=0.8)
Product.objects.create(name="15-inch Laptop", length=36, width=25, height=2, weight=2.1)
Product.objects.create(name="Desk Lamp", length=15, width=15, height=40, weight=1.2)

# Create Sample Boxes
ShippingBox.objects.create(name="Small Flat Rate", internal_length=25, internal_width=18, internal_height=8, max_weight_capacity=3.0, cost=1.25)
ShippingBox.objects.create(name="Medium Box", internal_length=40, internal_width=30, internal_height=15, max_weight_capacity=8.0, cost=2.50)
ShippingBox.objects.create(name="Large Box", internal_length=50, internal_width=35, internal_height=25, max_weight_capacity=15.0, cost=4.20)
ShippingBox.objects.create(name="Tall Box", internal_length=20, internal_width=20, internal_height=45, max_weight_capacity=6.0, cost=3.10)

print("Database seeded successfully with sample products and shipping boxes.")
