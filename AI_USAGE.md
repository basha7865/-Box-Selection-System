

1. AI Tool(s) Used :
Gemini Ai  

2. Prompts Given :
Prompt 1 (System Architecture & Overview):

"i want to develop a system that it recommends shipping boxes. Each product has dimensions and weight. Shipping boxes also contain inner measurements like internal dimensions, maximum weight capacity, and cost. please generate an overview of how the workflow works in this system . Your task is to design and build a small Django-based system that recommends the most suitable box for an order."

Prompt 2 (Initial Code Request):

"Now give me the whole code to run in my Visual Studio"

Prompt 3 (Full-Stack Request):

"Provide a full-stack project"

3. Output Accepted
Django Backend Models & Logic: Accepted the overall DB schema for Product and ShippingBox, along with helper properties (volume, internal_volume).

Recommendation Algorithm (services.py): Accepted the combined filtering approach checking hard physical boundaries (max_length, max_width, max_height), total weight limits, and minimum cost sorting via Python’s min() with a key function.

REST API Endpoint Structure: Accepted using Django view handlers (api_products, api_boxes, api_recommend) receiving and responding with standard JSON payloads.

Single-Page HTML Dashboard: Accepted the unified index.html layout utilizing vanilla JavaScript Fetch API to interact seamlessly with Django views without requiring external setup like React or Vue.

4. Output Rejected or Modified
Fragmented Setup Instructions: Rejected original snippets that required separate API clients  to demonstrate utility. Modified by replacing them with a fully integrated HTML/JS single-page application  running straight out of Django's native template engine.

Raw Django Rest Framework (DRF) Boilerplate: Rejected introducing heavy dependencies like djangorestframework or serializers to avoid setup friction for running directly in Visual Studio Code. Modified to pure Django built-in tools (JsonResponse, json.loads).

5. Mistakes the AI Made (And Corrected)
Bounding Volume vs. Spatial Fitting Assumption: The initial heuristic checks total volume (sum of item volumes <= box internal volume) and maximum single dimensions. However, this is a simplified calculation: multiple items side-by-side might exceed box dimensions even if total volume fits.

Correction/Note: Highlighted standard volumetric filtering while adding context on 3D Bin Packing extensions (py3dbp) for real-world orientation constraints.

CSRF Exemption: Using @csrf_exempt on Django POST views simplifies quick local dev/testing in VS Code, but in production, real CSRF tokens (or Django Session auth) are required.

6. How the Final Code Was Verified
Syntactic & Structural Review: Inspected all import paths (django.shortcuts, django.http, django.db) to ensure compliance with Django 4.x/5.x specifications.

Logic Edge-Case Verification:

Empty Input: Handled via explicit if not products: return None checks.

No Suitable Box Found: Verified that an order exceeding all capacity parameters returns an appropriate 404 Not Found JSON message without throwing server exceptions (500).

Cheapest Selection: Verified logic checks min(valid_boxes, key=lambda box: box.cost) so tied candidates always fall back to the lowest financial cost for shipping.

Frontend Integration Flow: Traced DOM event handlers (productForm.onsubmit, boxForm.onsubmit, calculateBox) to confirm payload structures align precisely with key names expected by JSON. loads(request.body).
