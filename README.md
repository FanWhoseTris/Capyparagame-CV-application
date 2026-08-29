# 🐾 Capybara Head-Tilt Navigation Game

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)](https://google.github.io/mediapipe/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> *"An interactive computer vision-powered mini-game where you guide a chill capybara dodging boulders in real-time using head tilts, blending embedded intelligence with computer vision engineering."*

---

## 🚀 Architectural Overview & Concept

This project breaks away from traditional keyboard/mouse inputs by leveraging **Computer Vision (CV)** and **Machine Learning (ML)** inference. Utilizing **Google MediaPipe Face Mesh**, the application tracks facial landmark geometries in real-time via webcam feed. By calculating the Roll and Pitch vectors of the head tilt orientation, players steer the capybara dynamically to dodge incoming rock obstacles while unlocking professional portfolio metrics.

---

## 🛠️ Tech Stack & Dependencies

### Core Vision & Processing Pipeline
* **Python 3.8+** — Primary runtime environment.
* **OpenCV (`cv2`)** — High-performance real-time video capture, image processing, and rendering pipeline.
* **Google MediaPipe** — Ultra-lightweight machine learning pipeline for robust 3D face landmark estimation.
* **NumPy** — Vector math optimization for head orientation angle calculations.

### Game Engine & Frontend (if applicable)
* **HTML5 Canvas / Pygame / WebSockets** — Game rendering loop and physics collision handling.

---

## 🧠 How Head-Tilt Detection Works (Algorithmic Logic)

1. **Facial Landmark Extraction:** MediaPipe detects 468 3D facial landmarks from each video frame.
2. **Vector Calculation:** Key anchor points (e.g., eye corners, nose bridge, chin) are extracted to compute the spatial rotation matrix.
3. **Threshold Filtering:** The system calculates the roll angle ($\theta$). Crossing predefined sensitivity thresholds triggers directional control signals (`LEFT`, `RIGHT`, `JUMP/DUCK`).
4. **Game State Synchronization:** Control signals map instantly to the capybara's movement vector in the physics engine.

---

## ⚙️ Installation & Setup Guide

### Prerequisites
* Python 3.8 or higher installed on your machine.
* A working webcam.

### Step-by-Step Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/FanWhoseTris/Capyparagame-CV-application.git](https://github.com/FanWhoseTris/Capyparagame-CV-application.git)
   cd Capyparagame-CV-application
