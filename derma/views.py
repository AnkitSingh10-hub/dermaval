from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserAttempt, AssessmentImage
from derma.task import grade_student_attempt

class SubmitAssessmentView(APIView):
    permission_classes = [IsAuthenticated] # Ensure only logged-in students can submit

    def post(self, request):
        user = request.user
        
        # 1. Extract Core Data
        image_id = request.data.get('image_id')
        user_boxes = request.data.get('boxes') # List of coordinates
        
        # 2. Extract Research Metrics (The "PhD" Data)
        # Frontend must measure how many seconds they spent on the page
        time_taken = request.data.get('time_taken', 0.0) 
        
        # Did they classify it as "Inflamed" or "Non-Inflamed"?
        classification = request.data.get('classification', "Unknown") 

        # 3. Validation
        if not AssessmentImage.objects.filter(id=image_id).exists():
            return Response({"error": "Invalid Image ID"}, status=400)

        # 4. Save to Database (The "filing cabinet")
        attempt = UserAttempt.objects.create(
            user=user,
            assessment_image_id=image_id,
            user_boxes=user_boxes,
            time_taken_seconds=float(time_taken), # Save for Cognitive Load analysis
            user_classification=classification,   # Save for Diagnostic Reasoning analysis
            iou_score=None # Will be filled by Celery
        )

        # 5. Trigger the Async Worker (The "Muscle")
        # .delay() puts it in Redis so the user gets an instant response
        grade_student_attempt.delay(attempt.id)

        return Response({
            "message": "Submission received. Grading in progress...", 
            "attempt_id": attempt.id,
            "status": "processing"
        })
        
        
class AssessmentResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, attempt_id):
        try:
            attempt = UserAttempt.objects.get(id=attempt_id, user=request.user)
            
            if attempt.is_graded:
                # Return the full Research Report
                return Response({
                    "status": "complete",
                    "score": attempt.iou_score,
                    "feedback": attempt.detailed_report, # e.g. "You missed 2 cysts"
                    # Return the Ground Truths so the Frontend can draw the "Correct" boxes
                    # on top of the student's boxes for visual comparison
                    "ground_truth_boxes": attempt.assessment_image.ground_truth_labels
                })
            else:
                return Response({"status": "processing"})
                
        except UserAttempt.DoesNotExist:
            return Response({"error": "Attempt not found"}, status=404)        