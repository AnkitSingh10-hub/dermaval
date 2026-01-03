# assessments/utils.py

def calculate_iou(box_a, box_b):
    """
    Calculates Intersection over Union (IoU) between two boxes.
    Format expected: {'x': int, 'y': int, 'width': int, 'height': int}
    """
    # 1. Determine the coordinates of the intersection rectangle
    x_left   = max(box_a['x'], box_b['x'])
    y_top    = max(box_a['y'], box_b['y'])
    x_right  = min(box_a['x'] + box_a['width'], box_b['x'] + box_b['width'])
    y_bottom = min(box_a['y'] + box_a['height'], box_b['y'] + box_b['height'])

    # 2. Calculate area of intersection
    if x_right < x_left or y_bottom < y_top:
        return 0.0 # No overlap
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # 3. Calculate area of both individual boxes
    box_a_area = box_a['width'] * box_a['height']
    box_b_area = box_b['width'] * box_b['height']

    # 4. Calculate Union (Area A + Area B - Intersection)
    union_area = box_a_area + box_b_area - intersection_area

    # 5. Return Score (0.0 to 1.0)
    return intersection_area / union_area