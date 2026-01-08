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
    # Prevent division by zero
    if union_area == 0:
        return 0.0
    return intersection_area / union_area

def grade_submission(ground_truth_boxes, user_boxes, iou_threshold=0.5):
    """
    PhD-Grade Logic: Compares list of user boxes against list of correct boxes.
    
    Args:
        ground_truth_boxes (list): The correct answers.
        user_boxes (list): The student's drawings.
        iou_threshold (float): How accurate the box must be to count as a 'Hit' (standard is 0.5).
        
    Returns:
        dict: Detailed statistics for the Learning Curve.
    """
    true_positives = 0
    false_positives = 0
    
    # Keep track of which GT boxes have already been "found" 
    # so a student can't get points twice for the same spot.
    matched_gt_indices = set()

    # --- STEP 1: Check every box the User drew ---
    for u_box in user_boxes:
        best_iou = 0
        best_gt_idx = -1

        # Compare this user box against ALL ground truth boxes
        # to find the one it overlaps with the most.
        for i, gt_box in enumerate(ground_truth_boxes):
            # If this acne spot was already matched, skip it (Greedy Match)
            if i in matched_gt_indices:
                continue
                
            iou = calculate_iou(u_box, gt_box)
            if iou > best_iou:
                best_iou = iou
                best_gt_idx = i

        # --- STEP 2: Decide if it's a Hit or Miss ---
        if best_iou >= iou_threshold:
            # HIT: The user found a spot!
            true_positives += 1
            matched_gt_indices.add(best_gt_idx)
        else:
            # MISS: The user drew a box where there was nothing (Hallucination)
            false_positives += 1

    # --- STEP 3: Calculate what they missed ---
    total_lesions = len(ground_truth_boxes)
    false_negatives = total_lesions - len(matched_gt_indices)

    # --- STEP 4: Calculate Research Metrics ---
    # Precision: When they draw a box, how often is it right?
    # Recall: Out of all the acne spots, how many did they find?
    
    precision = 0.0
    if (true_positives + false_positives) > 0:
        precision = true_positives / (true_positives + false_positives)

    recall = 0.0
    if total_lesions > 0:
        recall = true_positives / total_lesions

    # F1 Score (Harmonic Mean) - Ideally used for the final grade
    f1_score = 0.0
    if (precision + recall) > 0:
        f1_score = 2 * (precision * recall) / (precision + recall)

    return {
        "iou_score": round(f1_score, 2),  # This is the simplified score we save to DB
        "detailed_report": {
            "total_lesions": total_lesions,
            "correct_finds": true_positives,
            "false_positives": false_positives, # Student saw things that weren't there
            "missed_lesions": false_negatives,  # Student missed these
            "precision": round(precision, 2),
            "recall": round(recall, 2)
        }
    }