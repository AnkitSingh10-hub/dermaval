from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from derma.models import AssessmentImage
from roboflow import Roboflow
import requests
import os

class Command(BaseCommand):
    help = 'Fetches images and AI-predictions from Roboflow to build the Training Database'

    def handle(self, *args, **kwargs):
        # 1. SETUP ROBOFLOW
        # (You get these from your Roboflow Dashboard)
        rf = Roboflow(api_key="YOUR_ROBOFLOW_API_KEY")
        project = rf.workspace().project("your-project-name")
        model = project.version(1).model

        # 2. DEFINE IMAGE SOURCE
        # For this script, let's say we have a local folder of raw images
        # In a real PhD setup, this might be an S3 bucket or a hospital folder
        image_folder = "./raw_images/" 

        self.stdout.write("Starting AI Ingestion...")

        for filename in os.listdir(image_folder):
            if not filename.endswith((".jpg", ".png")):
                continue

            file_path = os.path.join(image_folder, filename)
            
            # --- THE AI MOMENT ---
            # We pass the image to the Neural Network
            prediction = model.predict(file_path, confidence=40, overlap=30).json()
            
            # Prediction format from Roboflow:
            # {'predictions': [{'x': 100, 'y': 50, 'width': 20, 'height': 20, 'class': 'acne', 'confidence': 0.9}]}
            
            ground_truth_list = []
            
            # 3. CONVERT AI DATA TO DJANGO DATA
            for pred in prediction['predictions']:
                ground_truth_list.append({
                    "x": pred['x'],
                    "y": pred['y'],
                    "width": pred['width'],
                    "height": pred['height'],
                    "label": pred['class']
                })

            # 4. SAVE TO DATABASE
            # This allows the "Student" to grade themselves against the "AI's" knowledge
            with open(file_path, 'rb') as f:
                img_content = ContentFile(f.read())
                
                # Create the entry in your database
                assessment = AssessmentImage.objects.create(
                    diagnosis_class="Acne", # You can make this dynamic based on the majority label
                    ground_truth_labels=ground_truth_list,
                    metadata={"source": "Roboflow_Model_v1", "ai_confidence": 0.9}
                )
                
                # Save the image file to VersatileImageField
                assessment.image_file.save(filename, img_content, save=True)

            self.stdout.write(f"Ingested {filename} with {len(ground_truth_list)} lesions detected by AI.")

        self.stdout.write(self.style.SUCCESS('AI Ingestion Complete.'))