# 🖊️ Hand-written Digits Recognition

**Team size:** 4 people  
**Project Field:** Computer Vision, Image Processing, Convolutional Neural Networks (CNN), k-Nearest Neighbors (KNN), Classification Problem  

This project explores **handwritten digit classification** using both **CNN** and **KNN** approaches. It evaluates performance on both the MNIST dataset and human-generated input from a custom GUI drawing tool. Experiments include varying distance metrics, Gaussian filtering, dropout rates, and model size to analyze their effect on accuracy.  

A **pre-trained CNN model** is provided (`final_model.h5`) for real-time digit prediction, while additional experiments on KNN and KNN with Gaussian constraints are documented in Kaggle notebooks.

---

## 📊 Kaggle Notebooks

- [Compare Model](https://www.kaggle.com/code/namkdo/compare-model) – Compares CNN and KNN performance on human-drawn digits.  
- [Intro to CNN](https://www.kaggle.com/code/namkdo/introai-cnn) – Explores Convolutional Neural Networks for digit classification.  
- [Intro to KNN](https://www.kaggle.com/code/namkdo/introai-knn) – Explores k-Nearest Neighbors (KNN) for digit classification, including variations with Gaussian constraints.  

---

## 🗂️ Project Structure

### 🖥️ Main Application
- **`main.py`**  
  - GUI for drawing digits using `tkinter`.  
  - Predicts digits using **CNN** (`final_model.h5`).  
  - **Preprocessing steps:**  
    1. Crop the digit from the canvas.  
    2. Resize while preserving aspect ratio to 28×28.  
    3. Center the digit in a 28×28 image.  
    4. Normalize pixel values to [0, 1].  

### 🛠️ Utilities
- **`ultility/drawer.py`** – Draw digits and save as **28×28 grayscale images** in CSV.  
- **`ultility/show.py`** – Display human-drawn digits from `digit_data1.csv`.  
- **`ultility/showMNIST.py`** – Visualize MNIST dataset digits.  

### 💾 Data & Models
- **`digit_data1.csv`** – Human-generated digit dataset (cropped, resized, centered, flattened, labeled).  
- **`final_model.h5`** – Pre-trained CNN model for digit recognition. Trained on MNIST and augmented with human-drawn digits.  

---

## 🤖 Algorithms

### CNN (Used for Prediction)
- Architecture: Convolutional layers → MaxPooling → Dense → Softmax.  
- Input: 28×28 grayscale images.  
- Output: 10-class probability vector (digits 0–9).  
- Preprocessing ensures compatibility with training data.

### KNN (Used for Evaluation / Experimentation)
- Distance metrics tested: Euclidean, Manhattan.  
- Variations:  
  - Standard KNN on MNIST and human-generated data.  
  - KNN with Gaussian filtering to reduce noise.  
- Used to compare **real-time performance** against CNN predictions.  

---

## ⚡ How to Run

> ⚠️ TensorFlow does not support Python 3.13. Use Python 3.11 or 3.12.

1. **Create a virtual environment (Python 3.11 recommended):**  
   ```bash
   python3.11 -m venv .venv
   ```

2. **Activate the virtual environment:**
   * *Windows:*
   ```bash
   .venv\Scripts\activate
   ```

   * *Linux/Mac:*
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r req.txt
   ```

4. **Run the main application:**
   ```bash
   python main.py
   ```

5. **Save custom digits using the drawer utility:**
   ```bash
   python ultility/drawer.py
   ```

6. **Visualize datasets:**
   ```bash
   python ultility/show.py       # For human-drawn digits
   python ultility/showMNIST.py  # For MNIST digits
   ```

## 📌 Notes

* **Prediction Accuracy:** The CNN is robust to human input but may occasionally misclassify ambiguous strokes. Preprocessing ensures the drawn digit is centered and scaled consistently.

* **Evaluation:** KNN experiments analyze differences between distance-based and deep learning-based classification. This highlights the strengths and limitations of each approach for real-world input.