import sys
import cv2
import torch
import pickle
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

DATA_FILE = 'face_data.pkl'


class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                        path=r'C:\Users\17590\PycharmProjects\onnxcaffe\yolov5s.pt',
                                        trust_repo=True, force_reload=True)  # Load fine-tuned YOLOv5 model
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model: {e}")
            sys.exit(1)

        self.face_data = self.load_face_data()

    def initUI(self):
        self.setWindowTitle('Face Data Entry')

        self.layout = QVBoxLayout()

        self.btn_start = QPushButton('Start Detect', self)
        self.btn_start.clicked.connect(self.start_detection)
        self.layout.addWidget(self.btn_start)

        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.setLayout(self.layout)

    def start_detection(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open video device")
            self.timer.start(20)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start video capture: {e}")
            self.cap.release()

    def update_frame(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Failed to read frame from camera")

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
                        self.save_face(face)
                        self.cap.release()
                        self.timer.stop()
                        self.get_user_name(face)
                        return

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(convert_to_qt_format))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process frame: {e}")
            self.cap.release()
            self.timer.stop()

    def save_face(self, face):
        try:
            cv2.imwrite('detected_face.jpg', face)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save face image: {e}")

    def get_user_name(self, face):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            QMessageBox.information(self, "Information", f"User {text} data has been recorded.")
            self.face_data[text] = face
            self.save_face_data()

    def save_face_data(self):
        try:
            with open(DATA_FILE, 'wb') as f:
                pickle.dump(self.face_data, f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save face data: {e}")

    def load_face_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load face data: {e}")
                return {}
        else:
            return {}


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = FaceRecognitionApp()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
