from .models import ShippingBox

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
