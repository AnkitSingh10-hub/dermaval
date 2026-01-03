DermaEval: Human-AI Collaborative Training Platform
![alt text](https://img.shields.io/badge/Status-Prototype-green)
![alt text](https://img.shields.io/badge/Tech-Django%20|%20Vue%20|%20Docker-blue)
![alt text](https://img.shields.io/badge/Research-Human--Centered%20AI-orange)
DermaEval is an interactive educational platform designed to bridge the gap between theoretical dermatology study and clinical application. Acting as a "flight simulator" for medical trainees, the system utilizes Computer Vision (YOLOv8) not to replace the human diagnostician, but to act as an automated supervisor—providing real-time, quantitative feedback on a student's ability to identify and localize skin pathologies.
🎯 Research Motivation
Keywords: Human-in-the-loop Learning, Automated Skill Assessment, Computer Vision in Healthcare.
Traditional medical training relies heavily on "over-the-shoulder" mentorship, which is resource-intensive and subjective. This project explores Human-Centered AI by inverting the typical diagnostic workflow. Instead of the AI providing the diagnosis, the human provides the diagnosis, and the AI validates the spatial accuracy of that input.
Key Research Objectives:
Quantify Diagnostic Accuracy: Using Intersection over Union (IoU) metrics to mathematically grade a trainee's bounding box annotations against Ground Truth AI.
Longitudinal Skill Tracking: Visualizing the "Learning Curve" to identify if a user is improving over time or struggling with specific pathologies (e.g., confusing cysts with nodules).
Scalable Feedback: Enabling asynchronous, mass-training sessions without the need for immediate senior faculty supervision.
🏗 System Architecture
The application is containerized via Docker, ensuring reproducibility across environments. The stack is architected to handle heavy image processing tasks asynchronously without blocking the user interface.
Component	Role	Technology Stack
The "Eyes"	Computer Vision & Inference	Roboflow, PyTorch (YOLOv8), OpenCV
The "Face"	Interactive Frontend	Vue.js 3, Vue-Konva (Canvas), Tailwind CSS
The "Brain"	Backend API & Logic	Django REST Framework (DRF), NumPy
The "Muscle"	Async Task Queue	Celery, Redis
The "Home"	Infrastructure	Docker Compose, PostgreSQL
🔄 User Workflow & Methodology
1. The Interactive Assessment (Student Mode)
The user is presented with a raw dermatological image from the dataset. Using the Vue-Konva powered canvas interface, the user acts as the doctor, drawing bounding boxes around perceived anomalies (e.g., Acne, Rosacea, Melanoma).
2. The Asynchronous Validation Pipeline
Upon submission, the frontend dispatches the coordinate data to the Django backend.
The request is offloaded to a Celery worker to prevent server timeout.
The system retrieves the Ground Truth predictions from the Roboflow/YOLOv8 inference engine.
The Grading Algorithm: The system calculates the Intersection over Union (IoU) between the User's box (
B
u
B 
u
​
 
) and the AI's box (
B
g
t
B 
gt
​
 
).
I
o
U
=
Area
(
B
u
∩
B
g
t
)
Area
(
B
u
∪
B
g
t
)
IoU= 
Area(B 
u
​
 ∪B 
gt
​
 )
Area(B 
u
​
 ∩B 
gt
​
 )
​
 
Threshold Logic: If 
I
o
U
>
0.5
IoU>0.5
 and the Class Label matches, it is a True Positive. Otherwise, it is flagged as a False Positive or False Negative.
3. The Feedback Loop
The user receives immediate visual feedback. The "Teacher's" (AI) boxes are overlaid on the "Student's" boxes using color-coded indicators (Green = Correct, Red = Missed).
Chart.js visualizations update the user's profile, tracking accuracy percentages across different skin conditions over time.
🚀 Installation & Setup
This project utilizes uv for fast Python package management and Docker for orchestration.
Prerequisites
Docker & Docker Compose
Git
Quick Start
Clone the repository
code
Bash
git clone https://github.com/yourusername/dermaeval.git
cd dermaeval
Configure Environment
Create a .env file in the root directory (template provided in .env.example) and add your Roboflow API Key.
Build and Run
code
Bash
docker compose up --build
Access the Application
Frontend: http://localhost:8080
API Documentation: http://localhost:8000/api/schema/swagger-ui/
📂 Project Structure
code
Text
dermaeval/
├── app/                  # Django Backend
│   ├── api/              # DRF Serializers & ViewSets
│   ├── core/             # IoU Logic & Scoring Algorithms
│   └── tasks.py          # Celery Async Definitions
├── frontend/             # Vue.js Application
│   ├── src/components/   # Konva Canvas & Chart.js Components
│   └── src/views/        # Student Dashboard
├── docker-compose.yml    # Service Orchestration
├── Dockerfile            # Multi-stage Python build with uv
└── pyproject.toml        # Dependency management
🔮 Future Work
Heatmap Analysis: Aggregating data from multiple students to identify "confusing" lesions that trick the majority of trainees.
Adaptive Difficulty: Using Reinforcement Learning to serve harder images as the student's accuracy score improves.
👨‍💻 Author
Ankit Singh