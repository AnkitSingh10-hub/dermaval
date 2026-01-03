# DERMAEVAL: HUMAN-AI COLLABORATIVE TRAINING PLATFORM

![Status](https://img.shields.io/badge/STATUS-PROTOTYPE-green?style=for-the-badge)
![Tech](https://img.shields.io/badge/TECH-DJANGO_%7C_VUE_%7C_DOCKER-blue?style=for-the-badge)
![Research](https://img.shields.io/badge/RESEARCH-HUMAN--CENTERED_AI-orange?style=for-the-badge)

**DermaEval** is an interactive educational platform designed to bridge the gap between theoretical dermatology study and clinical application. Acting as a **"flight simulator"** for medical trainees, the system utilizes Computer Vision (YOLOv8) not to replace the human diagnostician, but to act as an automated supervisor—providing real-time, quantitative feedback on a student's ability to identify and localize skin pathologies.

---

## 🎯 RESEARCH MOTIVATION
*Keywords: Human-in-the-loop Learning, Automated Skill Assessment, Computer Vision in Healthcare.*

Traditional medical training relies heavily on "over-the-shoulder" mentorship, which is resource-intensive and subjective. This project explores **Human-Centered AI** by inverting the typical diagnostic workflow. Instead of the AI providing the diagnosis, the *human* provides the diagnosis, and the AI validates the spatial accuracy of that input.

### KEY RESEARCH OBJECTIVES:
1.  **Quantify Diagnostic Accuracy:** Using Intersection over Union (IoU) metrics to mathematically grade a trainee's bounding box annotations against Ground Truth AI.
2.  **Longitudinal Skill Tracking:** Visualizing the "Learning Curve" to identify if a user is improving over time or struggling with specific pathologies (e.g., confusing *cysts* with *nodules*).
3.  **Scalable Feedback:** Enabling asynchronous, mass-training sessions without the need for immediate senior faculty supervision.

---

## 🏗 SYSTEM ARCHITECTURE

The application is containerized via **Docker**, ensuring reproducibility across environments. The stack is architected to handle heavy image processing tasks asynchronously without blocking the user interface.

| COMPONENT | ROLE | TECHNOLOGY STACK |
| :--- | :--- | :--- |
| **The "Eyes"** | Computer Vision & Inference | **Roboflow, PyTorch (YOLOv8), OpenCV** |
| **The "Face"** | Interactive Frontend | **Vue.js 3, Vue-Konva (Canvas), Tailwind CSS** |
| **The "Brain"** | Backend API & Logic | **Django REST Framework (DRF), NumPy** |
| **The "Muscle"** | Async Task Queue | **Celery, Redis** |
| **The "Home"** | Infrastructure | **Docker Compose, PostgreSQL** |

---

## 🔄 USER WORKFLOW & METHODOLOGY

### 1. THE INTERACTIVE ASSESSMENT (STUDENT MODE)
The user is presented with a raw dermatological image from the dataset. Using the **Vue-Konva** powered canvas interface, the user acts as the doctor, drawing bounding boxes around perceived anomalies (e.g., Acne, Rosacea, Melanoma).

### 2. THE ASYNCHRONOUS VALIDATION PIPELINE
Upon submission, the frontend dispatches the coordinate data to the Django backend.
*   The request is offloaded to a **Celery** worker to prevent server timeout.
*   The system retrieves the Ground Truth predictions from the **Roboflow/YOLOv8** inference engine.
*   **The Grading Algorithm:** The system calculates the **Intersection over Union (IoU)** between the User's box ($B_u$) and the AI's box ($B_{gt}$).

$$ IoU = \frac{\text{Area}(B_u \cap B_{gt})}{\text{Area}(B_u \cup B_{gt})} $$

*   **Threshold Logic:** If $IoU > 0.5$ and the Class Label matches, it is a **True Positive**. Otherwise, it is flagged as a **False Positive** or **False Negative**.

### 3. THE FEEDBACK LOOP
The user receives immediate visual feedback. The "Teacher's" (AI) boxes are overlaid on the "Student's" boxes using color-coded indicators (Green = Correct, Red = Missed).
**Chart.js** visualizations update the user's profile, tracking accuracy percentages across different skin conditions over time.

---

## 🚀 INSTALLATION & SETUP

This project utilizes `uv` for fast Python package management and Docker for orchestration.

### PREREQUISITES
*   Docker & Docker Compose
*   Git

### QUICK START

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/dermaeval.git
cd dermaeval