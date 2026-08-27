import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ShippingBox  # <-- Corrected model name

def dashboard_view(request):
    return render(request, 'index.html')

@csrf_exempt
def manage_boxes_api(request):
    """ GET all boxes or POST a new box """
    if request.method == 'GET':
        boxes = list(ShippingBox.objects.values(
            'id', 'name', 'internal_length', 'internal_width', 
            'internal_height', 'max_weight_capacity', 'cost'
        ))
        for b in boxes:
            b['cost'] = float(b['cost'])
        return JsonResponse({'boxes': boxes}, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            box = ShippingBox.objects.create(
                name=data['name'],
                internal_length=float(data['length']),
                internal_width=float(data['width']),
                internal_height=float(data['height']),
                max_weight_capacity=float(data['max_weight']),
                cost=float(data['cost'])
            )
            return JsonResponse({'message': 'Box added successfully', 'id': box.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def box_detail_api(request, box_id):
    """ PUT (update) or DELETE a specific box """
    try:
        box = ShippingBox.objects.get(id=box_id)
    except ShippingBox.DoesNotExist:
        return JsonResponse({'error': 'Box not found'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            box.name = data.get('name', box.name)
            box.internal_length = float(data.get('length', box.internal_length))
            box.internal_width = float(data.get('width', box.internal_width))
            box.internal_height = float(data.get('height', box.internal_height))
            box.max_weight_capacity = float(data.get('max_weight', box.max_weight_capacity))
            box.cost = float(data.get('cost', box.cost))
            box.save()
            return JsonResponse({'message': 'Box updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        box.delete()
        return JsonResponse({'message': 'Box deleted successfully'})