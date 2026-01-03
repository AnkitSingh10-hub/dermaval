import os
import json
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from derma.models import AssessmentImage 

class Command(BaseCommand):
    help = 'Loads Roboflow COCO data into the database'

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str, help='Path to the train/valid/test folder')

    def handle(self, *args, **kwargs):
        folder_path = kwargs['folder_path']
        json_path = os.path.join(folder_path, '_annotations.coco.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"JSON not found at: {json_path}"))
            return

        self.stdout.write(f"Reading metadata from {json_path}...")

        with open(json_path, 'r') as f:
            data = json.load(f)

        # Map Image IDs to Filenames
        images_map = {img['id']: img['file_name'] for img in data['images']}

        # Group Annotations
        annotations_map = {}
        for ann in data['annotations']:
            image_id = ann['image_id']
            bbox = ann['bbox'] # [x, y, w, h]
            
            clean_box = {
                "x": int(bbox[0]),
                "y": int(bbox[1]),
                "width": int(bbox[2]),
                "height": int(bbox[3]),
                "label": "acne"
            }

            if image_id not in annotations_map:
                annotations_map[image_id] = []
            annotations_map[image_id].append(clean_box)

        count = 0
        for img_id, filename in images_map.items():
            
            source_image_path = os.path.join(folder_path, filename)
            destination_filename = f"assessments/{filename}"
            full_destination_path = os.path.join(settings.MEDIA_ROOT, 'assessments', filename)

            # Ensure directory exists
            os.makedirs(os.path.dirname(full_destination_path), exist_ok=True)

            # Copy file
            if os.path.exists(source_image_path):
                shutil.copy(source_image_path, full_destination_path)
            else:
                continue

            ground_truth = annotations_map.get(img_id, [])

            # --- FIX: Check for existing image by filename instead of title ---
            # We filter by image_file to avoid duplicates
            if not AssessmentImage.objects.filter(image_file=destination_filename).exists():
                AssessmentImage.objects.create(
                    image_file=destination_filename,
                    ground_truth_labels=ground_truth,
                    difficulty='medium'
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} images!"))