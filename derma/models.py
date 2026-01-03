
from django.db import models
from users.models import User

class AssessmentImage(models.Model):
    """The image the student sees."""
    image_file = models.ImageField(upload_to='assessments/')
    # Store the 'Correct' boxes as JSON. 
    # Example: [{"x": 10, "y": 10, "width": 50, "height": 50, "class": "acne"}]
    ground_truth_labels = models.JSONField() 
    difficulty = models.CharField(max_length=20, default='easy')

class UserAttempt(models.Model):
    """The student's submission."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment_image = models.ForeignKey(AssessmentImage, on_delete=models.CASCADE)
    # Store the student's boxes
    user_boxes = models.JSONField() 
    # Store the calculated score
    iou_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)