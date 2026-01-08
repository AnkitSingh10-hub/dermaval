from django.db import models
from users.models import User
from core.models import TimeStampedModel, SoftDeleteModal

# --- NEW IMPORTS ---
from versatileimagefield.fields import VersatileImageField, PPOIField

class AssessmentImage(SoftDeleteModal, TimeStampedModel):
    """
    The 'Ground Truth' data.
    """
    # REPLACED: models.ImageField -> VersatileImageField
    image_file = VersatileImageField(
        'Image',
        upload_to='assessments/',
        ppoi_field='image_ppoi' # Links to the field below
    )
    
    # Stores the "Center point" of the image (useful for automatic cropping)
    image_ppoi = PPOIField()
    
    # Research Metric: Diagnosis Class
    diagnosis_class = models.CharField(max_length=50, null=True,blank=True, help_text="e.g. Acne, Rosacea, Melanoma")
    
    # The Correct Answer Coordinates
    ground_truth_labels = models.JSONField(null=True,blank=True,) 
    
    # Research Metric: Image Metadata
    metadata = models.JSONField(default=dict, help_text="e.g. {'lighting': 'poor', 'zoom': '10x'}")

    def __str__(self):
        return f"{self.diagnosis_class} - ID:{self.id}"


class UserAttempt(SoftDeleteModal, TimeStampedModel):
    """
    The Data Collection Point.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="derma_attempts")
    
    # Fixed String Reference
    assessment_image = models.ForeignKey('AssessmentImage', on_delete=models.CASCADE)
    
    user_boxes = models.JSONField(null=True,blank=True,help_text="Student's drawn coordinates")
    
    # PhD METRICS
    time_taken_seconds = models.FloatField(null=True,blank=True,help_text="Reaction time in seconds")
    user_classification = models.CharField(max_length=50, blank=True, null=True)

    # GRADING RESULTS
    iou_score = models.FloatField(null=True, blank=True)
    detailed_report = models.JSONField(null=True, blank=True)
    is_graded = models.BooleanField(default=False)
    
    def __str__(self):
        # Handle case where image might be None or Deleted
        img_name = self.assessment_image.diagnosis_class if self.assessment_image else "Deleted Image"
        return f"{self.user.username} attempt on {img_name}"