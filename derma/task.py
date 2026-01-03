from dermapj.celery import task
from .models import UserAttempt, AssessmentImage
from derma.utils import calculate_iou
import json

@task
def grade_student_attempt(attempt_id):
    attempt = UserAttempt.objects.get(id=attempt_id)
    ground_truth = attempt.assessment_image.ground_truth_labels
    student_boxes = attempt.user_boxes
    
    
    total_iou = 0
    matches = 0
    
    
    for s_box in student_boxes:
        s_vec = [s_box['x'], s_box['y'], s_box['width'], s_box['height']]
        best_match_score = 0
        
        for gt_box in ground_truth:
            gt_vec = [gt_box['x'], gt_box['y'], gt_box['width'], gt_box['height']]
            score = calculate_iou(s_vec, gt_vec)
            if score > best_match_score:
                best_match_score = score
        
        if best_match_score > 0.5: 
            total_iou += best_match_score
            matches += 1

    final_score = (total_iou / len(ground_truth)) * 100 if ground_truth else 0
    
    attempt.iou_score = final_score
    attempt.save()
    
    return f"Grading Complete. Score: {final_score}"