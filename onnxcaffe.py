import sys
import os
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage

class ObjectDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model_file = r'C:\Users\17590\PycharmProjects\onnxcaffe\deployssd\MobileNetSSD_deploy.caffemodel'
        self.config_file = r'C:\Users\17590\PycharmProjects\onnxcaffe\deployssd\MobileNetSSD_deploy.prototxt'

        # 打印路径以进行调试
        print(f'模型文件路径: {self.model_file}')
        print(f'配置文件路径: {self.config_file}')

        # 检查文件是否存在
        if not os.path.isfile(self.model_file):
            print(f'错误: 模型文件在 {self.model_file} 处未找到')
        if not os.path.isfile(self.config_file):
            print(f'错误: 配置文件在 {self.config_file} 处未找到')

        # 尝试加载网络
        try:
            self.net = cv2.dnn.readNetFromCaffe(self.config_file, self.model_file)
            print('网络成功加载')
        except cv2.error as e:
            print(f'cv2.error: {e}')

    def initUI(self):
        self.setWindowTitle('Object Detection')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.button = QPushButton('选择图片', self)
        self.button.clicked.connect(self.open_image)

        self.label = QLabel(self)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.jpg *.jpeg *.png)", options=options)
        if file_name:
            self.detect_objects(file_name)

    def detect_objects(self, image_path):
        img = cv2.imread(image_path)
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # 调整阈值
                class_id = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")

                label = "???"
                color = (0, 255, 0)  # Default color for unknown

                if class_id == 7:  # 假设 7 是模型中汽车的标签
                    label = f'Car: {confidence:.2f}'
                    color = (255, 0, 0)
                elif class_id == 15:  # 假设 15 是模型中人的标签
                    label = f'Person: {confidence:.2f}'
                    color = (0, 255, 0)

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ObjectDetectionApp()
    ex.show()
    sys.exit(app.exec_())
