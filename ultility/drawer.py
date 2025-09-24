import sys
import os
import csv
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtGui import QPainter, QPen, QImage, QColor
from PySide6.QtCore import Qt, QPoint

canvas_size = 280  # 10x scale for better drawing
img_size = 28      # Target image size
save_path = "../digit_data1.csv"

class DigitDrawer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Draw a Digit")
        self.setFixedSize(canvas_size, canvas_size + 50)

        # Canvas image
        self.image = QImage(canvas_size, canvas_size, QImage.Format_Grayscale8)
        self.image.fill(0)

        self.drawing = False
        self.last_point = QPoint()

        # Layouts
        main_layout = QVBoxLayout(self)
        canvas_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        # Label and entry
        self.label = QLabel("Enter Label:")
        self.entry = QLineEdit()
        self.entry.setFixedWidth(30)

        # Buttons
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_canvas)
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_digit)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.label)
        btn_layout.addWidget(self.entry)

        main_layout.addLayout(canvas_layout)
        main_layout.addLayout(btn_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.position.toPoint()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.image)
            pen = QPen(QColor(255, 255, 255), 12, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.position.toPoint())
            self.last_point = event.position.toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def clear_canvas(self):
        self.image.fill(0)
        self.update()

    def save_digit(self):
        label_text = self.entry.text()
        if not label_text.isdigit():
            print("Please enter a digit label (0-9).")
            return
        label = int(label_text)

        # Convert QImage to PIL-like numpy array
        arr = np.array(self.image.bits()).reshape(canvas_size, canvas_size).astype(np.float32)

        # Crop bounding box
        coords = np.argwhere(arr > 0)
        if coords.size == 0:
            print("No digit drawn.")
            return
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0)
        cropped = arr[y0:y1+1, x0:x1+1]

        # Resize keeping aspect ratio
        max_dim = max(cropped.shape)
        scale = img_size / max_dim
        new_size = (int(cropped.shape[1] * scale), int(cropped.shape[0] * scale))
        from PIL import Image
        pil_img = Image.fromarray(cropped).resize(new_size, Image.Resampling.LANCZOS)

        # Center on 28x28
        new_img = Image.new("L", (img_size, img_size), color=0)
        upper_left = ((img_size - new_size[0]) // 2, (img_size - new_size[1]) // 2)
        new_img.paste(pil_img, upper_left)

        # Flatten and save
        flat = np.asarray(new_img).flatten()
        row = [label] + flat.tolist()
        write_header = not os.path.exists(save_path)
        with open(save_path, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["label"] + [f"p{i}" for i in range(784)])
            writer.writerow(row)

        print(f"Saved digit '{label}' to {save_path}")
        self.clear_canvas()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitDrawer()
    window.show()
    sys.exit(app.exec())
