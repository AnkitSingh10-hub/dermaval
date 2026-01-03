
from django.db import models
from users.models import User
from derma.utils import *
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
    
    
    def save(self, *args, **kwargs):
        """
        Automatic Grading Logic:
        When .save() is called, compare user_boxes to ground_truth_labels
        """
        correct_boxes = self.assessment_image.ground_truth_labels
        
        student_boxes = self.user_boxes

        
        if correct_boxes and student_boxes:
            score = calculate_iou(correct_boxes[0], student_boxes[0])
            self.iou_score = score
        else:
            self.iou_score = 0.0

        super().save(*args, **kwargs)