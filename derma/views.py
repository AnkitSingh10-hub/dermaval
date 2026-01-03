from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from derma.models import AssessmentImage, UserAttempt
from derma.task import grade_student_attempt

class SubmitAssessmentView(APIView):
    def post(self, request):
        user = request.user
        image_id = request.data.get('image_id')
        user_boxes = request.data.get('boxes') 

        attempt = UserAttempt.objects.create(
            user=user,
            assessment_image_id=image_id,
            user_boxes=user_boxes,
            iou_score=None 
        )

        grade_student_attempt.delay(attempt.id)

        return Response({"message": "Assessment submitted! AI is grading...", "attempt_id": attempt.id})
    
    