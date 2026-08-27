Smart Shipping Box Selection System

A full-stack Django application that dynamically calculates and recommends the most cost-effective shipping box for an order based on item dimensions, combined volume, total weight, and box capacity limits.

---

## 🚀 Features

- **Automated Box Recommendation**: Analyzes total item weight, individual bounding dimensions, and cumulative volume to find the cheapest suitable box.
- **Built-in Interactive Dashboard**: Single-page web UI (HTML5/Vanilla JS) to manage products, create box profiles, and run instant recommendation tests.
- **RESTful API**: Lightweight JSON API endpoints for quick integration into e-commerce backends or warehouse management systems.
- **Zero Heavy Dependencies**: Built using pure Django without requiring external frameworks like React, Vue, or Django Rest Framework.

---

## 🛠️ System Architecture & Workflow

[ Customer Order ] ➡️ [ Extract Product Dimensions & Weight ]
│
▼
[ Aggregate Totals & Max Bounds ]
│
▼
[ Database Filter: Capacity & Physical Dimensions ]
│
▼
[ Sort Valid Candidates by Lowest Cost ]
│
▼
[ Optimal Box Recommendation ]


1. **Aggregation**: Calculates total weight, total cumulative volume, and maximum individual length, width, and height of items in an order.
2. **Hard Filtering**: Queries database for shipping boxes where:
   - `max_weight_capacity` ≥ Total Order Weight
   - `internal_length`, `internal_width`, `internal_height` ≥ Item Max Length, Width, Height
3. **Volume Validation**: Ensures candidate box `internal_volume` ≥ Total Order Cumulative Volume.
4. **Cost Optimization**: Ranks valid boxes by `cost` in ascending order and returns the cheapest option.

---


## 📂 Repository Structure

```text
.
├── config/
│   ├── settings.py      # Django Project Settings
│   ├── urls.py          # Root URL Routing
│   └── wsgi.py          # WSGI Deployment Config
├── recommender/
│   ├── templates/
│   │   └── index.html   # Interactive Single Page Frontend
│   ├── models.py        # Product & ShippingBox Database Schemas
│   ├── services.py      # Core Box Recommendation Logic
│   ├── views.py         # Web & API Request Handlers
│   └── urls.py          # App Endpoint Routes
├── manage.py            # Django CLI Utility
└── README.md            # System Documentation


Installation & Setup
Prerequisites
Python 3.8+

Git

Quickstart Guide
Clone the repository:

Bash
git clone git@github.com:basha7865/-Box-Selection-System.git
cd -Box-Selection-System
Create and activate a virtual environment:

Bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python -m venv venv
source venv/bin/activate
Install Django:

Bash
pip install django
Apply database migrations:

Bash
python manage.py makemigrations
python manage.py migrate
Start the development server:

Bash
python manage.py runserver
Open in browser:
Navigate to http://127.0.0.1:8000/ to use the interactive dashboard.

📡 API Endpoints
1. Fetch / Create Products
Endpoint: /api/products/

Methods: GET, POST

POST Payload Example:

JSON
{
  "name": "Mechanical Keyboard",
  "length": 44.0,
  "width": 14.0,
  "height": 4.0,
  "weight": 1.2
}
2. Fetch / Create Shipping Boxes
Endpoint: /api/boxes/

Methods: GET, POST

POST Payload Example:

JSON
{
  "name": "Medium Shipping Box",
  "internal_length": 50.0,
  "internal_width": 20.0,
  "internal_height": 10.0,
  "max_weight_capacity": 5.0,
  "cost": 2.50
}
3. Recommend Box for Order
Endpoint: /api/recommend/

Method: POST

Request Body:

JSON
{
  "product_ids": [1, 2]
}
Response Example:

JSON
{
  "found": true,
  "box_name": "Medium Shipping Box",
  "cost": 2.50,
  "dimensions": "50.0 x 20.0 x 10.0 cm",
  "max_weight": 5.0
}
💡 AI-Assisted Development & Verification Analysis
🤖 AI Engine Used
Gemini (Google AI)

📋 AI Generation Log
Prompts Provided:

System Overview: Architecture and algorithmic approach for box recommendation based on dimensions, weight, and box inner constraints.

Core Backend: Code structure including Django models, service module, and API views.

Full-Stack Integration: Interactive single-page UI embedded directly inside Django templates.

Accepted Outputs:

Product and ShippingBox database schemas with property decorators for volume evaluation.

Multi-stage filtering algorithm (services.py) using min() with a cost key function.

Lightweight single-page frontend interface using vanilla JavaScript fetch().

Rejected / Modified Outputs:

Rejected: Raw Django REST Framework (DRF) serializers to avoid adding unnecessary package dependencies.

Modified: Replaced external API testing instructions (e.g., Postman) with a native browser dashboard for direct manual testing.

Identified Edge Cases & Mitigations:

Spatial vs. Volumetric Fitting: Basic volumetric logic can yield false positives if items cannot physically stack due to rotation limitations. Mitigation note: For advanced spatial packing requirements, integration with a 3D Bin Packing library (such as py3dbp) is recommended.

CSRF Handling: Applied @csrf_exempt on local API endpoints for frictionless testing in VSC; standard CSRF middleware tokens should be enabled for production deployments.

Verification Steps:

Syntax & Import Validation: Tested standard Django 4.x/5.x request-response flows.

Boundary Testing: Verified behavior when no boxes meet item criteria (returning clear 404 responses instead of server crashes).

Cost Minimization Logic: Confirmed sorting selects the lowest-priced valid box when multiple candidates fit spatial constraints.
