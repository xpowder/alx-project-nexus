"""
Management command to load sample products and categories into the database.

Usage:
    python manage.py load_sample_data
"""

from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Load sample products and categories into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products and categories before loading',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write(self.style.SUCCESS('Loading sample data...'))

        # Create Categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel'
            },
            {
                'name': 'Books',
                'description': 'Books and reading materials'
            },
            {
                'name': 'Home & Kitchen',
                'description': 'Home essentials and kitchen appliances'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sports equipment and outdoor gear'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create Products
        products_data = [
            # Electronics
            {
                'name': 'Laptop - Dell XPS 15',
                'description': 'High-performance laptop with Intel i7 processor, 16GB RAM, 512GB SSD, 15.6" FHD display. Perfect for professionals and students.',
                'price': 1299.99,
                'stock': 25,
                'category': 'Electronics',
                'brand': 'Dell',
                'weight': 2.1
            },
            {
                'name': 'Wireless Mouse - Logitech MX Master 3',
                'description': 'Ergonomic wireless mouse with advanced sensor technology, long battery life, and customizable buttons.',
                'price': 99.99,
                'stock': 150,
                'category': 'Electronics',
                'brand': 'Logitech',
                'weight': 0.141
            },
            {
                'name': 'Bluetooth Headphones - Sony WH-1000XM5',
                'description': 'Industry-leading noise cancellation, exceptional sound quality, 30-hour battery life, comfortable over-ear design.',
                'price': 399.99,
                'stock': 40,
                'category': 'Electronics',
                'brand': 'Sony',
                'weight': 0.25
            },
            {
                'name': 'Smartphone - iPhone 15 Pro',
                'description': 'Latest iPhone with A17 Pro chip, 256GB storage, Pro camera system, and titanium design.',
                'price': 999.99,
                'stock': 30,
                'category': 'Electronics',
                'brand': 'Apple',
                'weight': 0.187
            },
            {
                'name': 'Tablet - iPad Air',
                'description': '10.9-inch Liquid Retina display, M2 chip, 256GB storage, supports Apple Pencil and Magic Keyboard.',
                'price': 749.99,
                'stock': 20,
                'category': 'Electronics',
                'brand': 'Apple',
                'weight': 0.461
            },
            
            # Clothing
            {
                'name': 'Classic Cotton T-Shirt',
                'description': '100% cotton t-shirt, comfortable fit, available in multiple colors. Perfect for everyday wear.',
                'price': 24.99,
                'stock': 200,
                'category': 'Clothing',
                'brand': 'Premium Basics',
                'weight': 0.15
            },
            {
                'name': 'Denim Jeans - Classic Fit',
                'description': 'Classic fit denim jeans with stretch fabric, comfortable waistband, multiple sizes available.',
                'price': 79.99,
                'stock': 100,
                'category': 'Clothing',
                'brand': 'Denim Co',
                'weight': 0.5
            },
            {
                'name': 'Running Shoes - Nike Air Max',
                'description': 'Lightweight running shoes with air cushioning, breathable mesh upper, perfect for daily runs.',
                'price': 129.99,
                'stock': 75,
                'category': 'Clothing',
                'brand': 'Nike',
                'weight': 0.3
            },
            {
                'name': 'Winter Jacket - Waterproof',
                'description': 'Waterproof winter jacket with insulation, hood, multiple pockets, ideal for cold weather.',
                'price': 149.99,
                'stock': 50,
                'category': 'Clothing',
                'brand': 'Outdoor Gear',
                'weight': 0.8
            },
            
            # Books
            {
                'name': 'The Complete Python Programming Guide',
                'description': 'Comprehensive guide to Python programming from basics to advanced topics. Includes practical examples and projects.',
                'price': 49.99,
                'stock': 100,
                'category': 'Books',
                'brand': 'Tech Books',
                'weight': 0.6
            },
            {
                'name': 'Django for Professionals',
                'description': 'Learn Django framework for building scalable web applications. Real-world examples and best practices.',
                'price': 54.99,
                'stock': 80,
                'category': 'Books',
                'brand': 'Tech Books',
                'weight': 0.7
            },
            {
                'name': 'Clean Code: A Handbook',
                'description': 'Learn to write clean, maintainable code. Essential reading for all software developers.',
                'price': 44.99,
                'stock': 120,
                'category': 'Books',
                'brand': 'Programming Books',
                'weight': 0.55
            },
            
            # Home & Kitchen
            {
                'name': 'Stainless Steel Coffee Maker',
                'description': '12-cup programmable coffee maker with thermal carafe, auto-shutoff, and brewing strength control.',
                'price': 89.99,
                'stock': 60,
                'category': 'Home & Kitchen',
                'brand': 'Kitchen Pro',
                'weight': 2.5
            },
            {
                'name': 'Air Fryer - 6 Quart',
                'description': 'Large capacity air fryer, digital display, multiple cooking modes, easy to clean, healthier cooking.',
                'price': 119.99,
                'stock': 45,
                'category': 'Home & Kitchen',
                'brand': 'Kitchen Pro',
                'weight': 4.2
            },
            {
                'name': 'Smart TV - 55" 4K Ultra HD',
                'description': '55-inch 4K Ultra HD Smart TV with HDR, streaming apps built-in, voice control, wall mountable.',
                'price': 599.99,
                'stock': 30,
                'category': 'Home & Kitchen',
                'brand': 'TechVision',
                'weight': 18.5
            },
            
            # Sports & Outdoors
            {
                'name': 'Yoga Mat - Premium',
                'description': 'Extra thick yoga mat with non-slip surface, easy to clean, perfect for yoga and exercise.',
                'price': 39.99,
                'stock': 90,
                'category': 'Sports & Outdoors',
                'brand': 'FitLife',
                'weight': 1.2
            },
            {
                'name': 'Water Bottle - Insulated',
                'description': '32oz insulated stainless steel water bottle, keeps drinks cold for 24 hours, leak-proof design.',
                'price': 29.99,
                'stock': 150,
                'category': 'Sports & Outdoors',
                'brand': 'Hydra',
                'weight': 0.4
            },
            {
                'name': 'Dumbbell Set - Adjustable',
                'description': 'Pair of adjustable dumbbells, 5-50lbs each, compact design, perfect for home workouts.',
                'price': 199.99,
                'stock': 25,
                'category': 'Sports & Outdoors',
                'brand': 'FitLife',
                'weight': 25.0
            },
            {
                'name': 'Bicycle - Mountain Bike',
                'description': '21-speed mountain bike with front suspension, disc brakes, suitable for trails and city riding.',
                'price': 449.99,
                'stock': 15,
                'category': 'Sports & Outdoors',
                'brand': 'Trail Rider',
                'weight': 15.0
            },
        ]

        created_count = 0
        updated_count = 0

        for product_data in products_data:
            category = categories[product_data.pop('category')]
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    **product_data,
                    'category': category
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created: {product.name}')
            else:
                # Update existing product
                for key, value in product_data.items():
                    setattr(product, key, value)
                product.category = category
                product.save()
                updated_count += 1
                self.stdout.write(f'  ↻ Updated: {product.name}')

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully loaded sample data!'))
        self.stdout.write(self.style.SUCCESS(f'  - Categories: {len(categories)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Products created: {created_count}'))
        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f'  - Products updated: {updated_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('\nYou can now view products at: http://localhost:8000/api/products/products/'))

