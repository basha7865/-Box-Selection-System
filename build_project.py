import os

files = {
    # App Config
    "recommender/apps.py": """from django.apps import AppConfig

class RecommenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommender'
""",
    # Models
    "recommender/models.py": """from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    length = models.FloatField(help_text="Length in cm")
    width = models.FloatField(help_text="Width in cm")
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")

    @property
    def volume(self):
        return self.length * self.width * self.height

    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height} cm, {self.weight}kg)"

class ShippingBox(models.Model):
    name = models.CharField(max_length=100)
    internal_length = models.FloatField(help_text="Internal length in cm")
    internal_width = models.FloatField(help_text="Internal width in cm")
    internal_height = models.FloatField(help_text="Internal height in cm")
    max_weight_capacity = models.FloatField(help_text="Max weight in kg")
    cost = models.DecimalField(max_digits=8, decimal_places=2, help_text="Cost in USD")

    @property
    def internal_volume(self):
        return self.internal_length * self.internal_width * self.internal_height

    def __str__(self):
        return f"{self.name} - ${self.cost}"
""",
    # Service Logic
    "recommender/services.py": """from .models import ShippingBox

def recommend_best_box(products):
    if not products:
        return None

    total_weight = sum(p.weight for p in products)
    total_volume = sum(p.volume for p in products)

    max_length = max(p.length for p in products)
    max_width = max(p.width for p in products)
    max_height = max(p.height for p in products)

    candidate_boxes = ShippingBox.objects.filter(
        max_weight_capacity__gte=total_weight,
        internal_length__gte=max_length,
        internal_width__gte=max_width,
        internal_height__gte=max_height
    )

    valid_boxes = [box for box in candidate_boxes if box.internal_volume >= total_volume]

    if not valid_boxes:
        return None

    return min(valid_boxes, key=lambda box: box.cost)
""",
    # Views & API
    "recommender/views.py": """import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, ShippingBox
from .services import recommend_best_box

def index(request):
    products = Product.objects.all()
    boxes = ShippingBox.objects.all()
    return render(request, 'recommender/index.html', {
        'products': products,
        'boxes': boxes
    })

@csrf_exempt
def recommend_box_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_ids = data.get("product_ids", [])
            
            products = list(Product.objects.filter(id__in=product_ids))
            if not products:
                return JsonResponse({"error": "No valid products selected."}, status=400)

            best_box = recommend_best_box(products)

            if best_box:
                return JsonResponse({
                    "recommended_box": best_box.name,
                    "cost": float(best_box.cost),
                    "internal_dimensions": {
                        "length": best_box.internal_length,
                        "width": best_box.internal_width,
                        "height": best_box.internal_height
                    },
                    "max_weight_capacity": best_box.max_weight_capacity,
                    "internal_volume": best_box.internal_volume
                })
            else:
                return JsonResponse({"message": "No single box can fit this order weight or dimensions."}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST requests allowed."}, status=405)
""",
    # Admin Interface
    "recommender/admin.py": """from django.contrib import admin
from .models import Product, ShippingBox

admin.site.register(Product)
admin.site.register(ShippingBox)
""",
    # Project Settings
    "config/settings.py": """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-box-recommender-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recommender',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""",
    # Routing URLs
    "config/urls.py": """from django.contrib import admin
from django.urls import path
from recommender.views import index, recommend_box_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/recommend-box/', recommend_box_view, name='recommend_box'),
]
""",
    # Seed Script for Database
    "seed.py": """import os
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
""",
    # Single-file HTML/CSS/JS Frontend Template
    "recommender/templates/recommender/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Packaging Recommender</title>
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --accent-hover: #0284c7;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --success: #22c55e;
            --error: #ef4444;
        }

        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }

        .container {
            max-width: 900px;
            width: 100%;
        }

        header {
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1rem;
        }

        h1 { margin: 0 0 0.5rem 0; font-size: 1.875rem; color: var(--accent); }
        p { margin: 0; color: var(--text-muted); }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.25rem;
        }

        h2 { font-size: 1.25rem; margin-top: 0; margin-bottom: 1rem; }

        .item-list {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 250px;
            overflow-y: auto;
        }

        .item-label {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.5rem;
            background: #0f172a;
            border-radius: 4px;
            border: 1px solid var(--border);
            cursor: pointer;
        }

        .btn {
            background-color: var(--accent);
            color: #000;
            font-weight: 600;
            border: none;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            transition: background-color 0.2s;
        }

        .btn:hover { background-color: var(--accent-hover); }

        .result-box {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 6px;
            display: none;
        }

        .result-box.success {
            background-color: rgba(34, 197, 94, 0.1);
            border: 1px solid var(--success);
            display: block;
        }

        .result-box.error {
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--error);
            display: block;
        }

        .badge {
            background-color: var(--border);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Box Recommendation System</h1>
            <p>Select products to compute optimal box sizes based on capacity, dimensions, and cost.</p>
        </header>

        <div class="grid">
            <div class="card">
                <h2>1. Select Products</h2>
                <div class="item-list">
                    {% for product in products %}
                    <label class="item-label">
                        <span>
                            <input type="checkbox" value="{{ product.id }}" class="product-select">
                            <strong>{{ product.name }}</strong>
                        </span>
                        <span class="badge">{{ product.length }}x{{ product.width }}x{{ product.height }}cm | {{ product.weight }}kg</span>
                    </label>
                    {% endfor %}
                </div>
                <button class="btn" onclick="getRecommendation()">Find Best Box</button>
            </div>

            <div class="card">
                <h2>2. Recommendation Result</h2>
                <div id="placeholder-text" style="color: var(--text-muted);">Select products on the left and submit to find a box match.</div>
                <div id="result-display" class="result-box"></div>
            </div>
        </div>
    </div>

    <script>
        async function getRecommendation() {
            const checkboxes = document.querySelectorAll('.product-select:checked');
            const ids = Array.from(checkboxes).map(cb => parseInt(cb.value));
            const resultDiv = document.getElementById('result-display');
            const placeholder = document.getElementById('placeholder-text');

            if (ids.length === 0) {
                resultDiv.className = 'result-box error';
                resultDiv.innerHTML = '<strong>Error:</strong> Please select at least one product.';
                placeholder.style.display = 'none';
                return;
            }

            try {
                const response = await fetch('/api/recommend-box/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ product_ids: ids })
                });

                const data = await response.json();
                placeholder.style.display = 'none';

                if (response.ok) {
                    resultDiv.className = 'result-box success';
                    resultDiv.innerHTML = `
                        <h3 style="margin-top:0; color: var(--success);">Best Match: ${data.recommended_box}</h3>
                        <p><strong>Cost:</strong> $${data.cost.toFixed(2)}</p>
                        <p><strong>Max Capacity:</strong> ${data.max_weight_capacity} kg</p>
                        <p><strong>Internal Dimensions:</strong> ${data.internal_dimensions.length} × ${data.internal_dimensions.width} × ${data.internal_dimensions.height} cm</p>
                    `;
                } else {
                    resultDiv.className = 'result-box error';
                    resultDiv.innerHTML = `<strong>Notice:</strong> ${data.message || data.error}`;
                }
            } catch (err) {
                resultDiv.className = 'result-box error';
                resultDiv.innerHTML = '<strong>System Error:</strong> Unable to connect to server.';
            }
        }
    </script>
</body>
</html>
"""
}

# Create Directories and Write Files
for path, content in files.items():
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Files created successfully.")