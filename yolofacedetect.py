import sys
import cv2
import torch
import pickle
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from skimage.metrics import structural_similarity as ssim

DATA_FILE = 'face_data.pkl'

class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                        path=r'C:\Users\17590\PycharmProjects\onnxcaffe\yolov5s.pt',
                                        trust_repo=True, force_reload=True)  # Load fine-tuned YOLOv5 model
        except Exception as e:
            self.show_error(f"Failed to load model: {e}")
            sys.exit(1)

        self.face_data = self.load_face_data()

    def initUI(self):
        self.setWindowTitle('Face Recognition')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.button = QPushButton('Start Detection', self)
        self.button.clicked.connect(self.start_detection)

        self.label = QLabel(self)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def start_detection(self):
        if not self.cap.isOpened():
            self.show_error("Could not open video device")
            return
        self.timer.start(20)

    def update_frame(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                self.show_error("Failed to read frame from camera")
                return

            results = self.model(frame)  # Perform detection
            labels, cords = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()

            for label, cord in zip(labels, cords):
                if label == 0:  # Label 0 typically indicates a person in YOLO models
                    if len(cord) != 5:
                        raise Exception(f"Expected 5 elements in cord, got {len(cord)}")
                    x1, y1, x2, y2, conf = cord
                    x1, y1, x2, y2 = int(x1 * frame.shape[1]), int(y1 * frame.shape[0]), int(x2 * frame.shape[1]), int(y2 * frame.shape[0])
                    if conf > 0.5:
                        face = frame[y1:y2, x1:x2]
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                        recognized = self.recognize_face(face)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, recognized, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(convert_to_qt_format))
        except Exception as e:
            self.show_error(f"Failed to process frame: {e}")
            self.cap.release()
            self.timer.stop()

    def recognize_face(self, face):
        # Simplified face recognition logic based on structural similarity
        highest_ssim = 0
        recognized_name = "Unknown user"
        face_resized = cv2.resize(face, (100, 100))  # Resize face to a fixed size for comparison

        for name, saved_face in self.face_data.items():
            saved_face = cv2.cvtColor(saved_face, cv2.COLOR_BGR2RGB)
            saved_face_resized = cv2.resize(saved_face, (100, 100))  # Resize saved face to match the size
            win_size = min(saved_face_resized.shape[0], saved_face_resized.shape[1], 7)
            if win_size % 2 == 0:
                win_size -= 1  # Ensure win_size is odd

            score, _ = ssim(saved_face_resized, face_resized, full=True, multichannel=True, win_size=win_size, channel_axis=2)
            if score > highest_ssim:
                highest_ssim = score
                recognized_name = name
        return recognized_name

    def load_face_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self.show_error(f"Failed to load face data: {e}")
                return {}
        else:
            return {}

    def show_error(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FaceRecognitionApp()
    ex.show()
    sys.exit(app.exec_())
