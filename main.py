import sys
import os
import numpy as np
from PIL import Image, ImageDraw
from tensorflow.keras.models import load_model
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PySide6.QtGui import QPainter, QPen, QImage, QColor
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QImage


# Load the trained model
MODEL_PATH = "final_model.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

model = load_model(MODEL_PATH)

canvas_size = 280  # Drawing canvas size
img_size = 28      # CNN input size


class DrawingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(canvas_size, canvas_size)
        self.setStyleSheet("background-color: black;")

        # For drawing
        self.image = QImage(self.size(), QImage.Format_Grayscale8)
        self.image.fill(Qt.black)
        self.last_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_point is not None:
            painter = QPainter(self.image)
            pen = QPen(Qt.white, 12, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = None

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def clear(self):
        self.image.fill(Qt.black)
        self.update()

    def get_pil_image(self):
        qimage = self.image.convertToFormat(QImage.Format.Format_RGB32)
        ptr = qimage.constBits()
        arr = np.frombuffer(ptr, dtype=np.uint8).copy()
        arr = arr.reshape(qimage.height(), qimage.width(), 4)  # BGRA

        # Convert to grayscale
        gray = np.dot(arr[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        pil_img = Image.fromarray(gray)

        return pil_img



class DigitRecognizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Draw a Digit (Qt🚀)")

        layout = QVBoxLayout()

        # Drawing area
        self.canvas = DrawingCanvas(self)
        layout.addWidget(self.canvas)

        # Buttons + result
        button_layout = QHBoxLayout()

        self.predict_btn = QPushButton("Predict")
        self.predict_btn.clicked.connect(self.predict_digit)
        button_layout.addWidget(self.predict_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.canvas.clear)
        button_layout.addWidget(self.clear_btn)

        self.label = QLabel("Prediction: ")
        button_layout.addWidget(self.label)

        self.result = QLabel("")
        self.result.setStyleSheet("font-size: 16px; font-weight: bold;")
        button_layout.addWidget(self.result)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def predict_digit(self):
        pil_img = self.canvas.get_pil_image()  # <- use the new fixed method
    
        bbox = pil_img.getbbox()
        if bbox is None:
            self.result.setText("No digit")
            return
    
        cropped = pil_img.crop(bbox)
    
        # Resize with aspect ratio
        max_dim = max(cropped.size)
        scale = img_size / max_dim
        new_size = tuple([int(dim * scale) for dim in cropped.size])
        resized = cropped.resize(new_size, Image.Resampling.LANCZOS)
    
        new_img = Image.new("L", (img_size, img_size), color=0)
        upper_left = ((img_size - new_size[0]) // 2, (img_size - new_size[1]) // 2)
        new_img.paste(resized, upper_left)
    
        img_arr = np.asarray(new_img).astype(np.float32)
        img_arr = img_arr.reshape(1, 28, 28, 1) / 255.0
    
        prediction = model.predict(img_arr, verbose=0)
        digit = np.argmax(prediction)
        confidence = np.max(prediction)
    
        self.result.setText(f"{digit} ({confidence*100:.2f}%)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitRecognizer()
    window.show()
    sys.exit(app.exec())
