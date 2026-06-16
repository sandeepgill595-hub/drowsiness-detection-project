# Drowsiness Detection System using Computer Vision

## Project Overview

This project is a real-time **Drowsiness Detection System** built using **Python, Streamlit, OpenCV, and MediaPipe**.

The system monitors a user's eyes through webcam input and detects signs of drowsiness by calculating the eye opening gap using facial landmarks.

When the eye gap falls below a defined threshold for a sustained period, the system classifies the user as **Drowsy**. Otherwise, the user is classified as **Awake**.

---

## Problem Statement

Driver or operator drowsiness is a major cause of accidents and reduced productivity.
This project aims to build a lightweight AI-based system that can detect drowsiness in real time and help improve safety.

---

## Features

* Real-time webcam monitoring
* Face landmark detection
* Eye gap calculation using Euclidean distance
* Drowsiness detection based on threshold
* Live status display:

  * Awake
  * Drowsy
* Interactive Streamlit interface

---

## Tech Stack

* Python
* Streamlit
* OpenCV
* MediaPipe
* NumPy

---

## Project Structure

```
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

```
git clone <your-github-link>
```

Move into project folder:

```
cd drowsiness_detection_project
```

Create virtual environment:

```
python -m venv venv
```

Activate virtual environment:

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run the Application

```
streamlit run app.py
```

---

## Author

Sandeep Gill
