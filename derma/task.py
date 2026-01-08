from dermapj.celery import shared_task
from .models import UserAttempt, AssessmentImage
from .utils import grade_submission # Import the advanced logic we just wrote
import json

@shared_task
def grade_student_attempt(attempt_id):
    """
    Async Task: 
    1. Fetches the attempt
    2. Runs the Greedy Matching Algorithm (Precision/Recall)
    3. Saves detailed metrics for the Learning Curve analysis
    """
    try:
        attempt = UserAttempt.objects.get(id=attempt_id)
    except UserAttempt.DoesNotExist:
        return f"Attempt {attempt_id} not found."

    # Get the raw JSON lists
    # Ensure they are Python lists/dicts, not strings
    ground_truth = attempt.assessment_image.ground_truth_labels
    student_boxes = attempt.user_boxes
    
    # --- THE PHD UPGRADE ---
    # Instead of a manual loop here, we call the advanced math function
    # that handles 'False Positives' and 'Precision/Recall'
    results = grade_submission(ground_truth, student_boxes)

    # Save the Research Metrics
    attempt.iou_score = results['iou_score'] # The F1 Score (0.0 to 1.0)
    
    # Save the granular data: {"false_positives": 2, "precision": 0.6, ...}
    attempt.detailed_report = results['detailed_report']
    
    attempt.is_graded = True
    attempt.save()

    # Log for debugging
    return f"Graded Attempt {attempt_id}: Score {attempt.iou_score}, Missed: {results['detailed_report']['missed_lesions']}"