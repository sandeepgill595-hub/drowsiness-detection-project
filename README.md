# Drowsiness Detection System using Computer Vision

## Project Overview
This project is a real-time **Drowsiness Detection System** built using **Python, OpenCV, and MediaPipe**.
The system monitors a user's eyes through webcam input in real time and detects signs of drowsiness by calculating the eye-opening gap using facial landmarks.
When the eye gap falls below a defined threshold for a sustained period, the system classifies the user as **Drowsy**. Otherwise, the user is classified as **Awake**.

---

## Problem Statement
Driver or operator drowsiness is a major cause of accidents and reduced productivity.
This project aims to build a lightweight AI-based system that can detect drowsiness in real time and help improve safety.

---

## Live Demo
Try the app directly in your browser — no installation needed:

🔗 [Launch Drowsiness Detection App](https://drowsiness-detection-project-5mmumc7gzydymo22fa46fd.streamlit.app)

Supported modes:
- **IMAGE** — Upload a photo to detect drowsiness
- **VIDEO** — Upload a video for frame-by-frame detection

---

## Features
* Real-time webcam monitoring
* Face landmark detection
* Eye gap calculation using Euclidean distance
* Drowsiness detection based on a threshold
* Live status display:
  * Awake 🟢
  * Drowsy 🔴

---

## Tech Stack
* Python
* OpenCV
* MediaPipe
* NumPy
* Streamlit

---

## Project Structure
```bash
drowsiness_detection_project/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation
Clone the repository:
```bash
git clone https://github.com/sandeepgill595-hub/drowsiness-detection-project.git
```
Move into the project folder:
```bash
cd drowsiness_detection_project
```
Create a virtual environment:
```bash
python -m venv venv
```
Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the app locally:
```bash
streamlit run app.py
```

---

## Author
Sandeep Gill
