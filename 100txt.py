import cv2
import numpy as np
import os

class ObjectDetection:
    def __init__(self):
        self.model_file = r'deployssd/MobileNetSSD_deploy.caffemodel'
        self.config_file = r'deployssd/MobileNetSSD_deploy.prototxt'
        self.net = cv2.dnn.readNetFromCaffe(self.config_file, self.model_file)
        self.classes = {7: 'car', 15: 'person'}  # Assuming 7 is car and 15 is person

    def detect_objects(self, image_path):
        img = cv2.imread(image_path)
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        results = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Threshold can be adjusted
                class_id = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                if class_id in self.classes:
                    label = self.classes[class_id]
                    results.append((label, confidence, (x1, y1, x2, y2)))
        return results

    def process_images(self, input_dir, output_file):
        with open(output_file, 'w') as f:
            for i in range(100):
                image_path = os.path.join(input_dir, f"{i}.jpg")
                if os.path.exists(image_path):
                    detections = self.detect_objects(image_path)
                    for j, (label, confidence, box) in enumerate(detections):
                        x1, y1, x2, y2 = box
                        f.write(f"{i}_jpg_{j}_{label}:[label: {label}, {confidence:.2f}, {x1}, {y1}, {x2}, {y2}]\n")

if __name__ == "__main__":
    input_dir = r"C:\Users\17590\PycharmProjects\onnxcaffe\100txt"
    output_file = r"C:\Users\17590\PycharmProjects\onnxcaffe\picture\ssdlable.txt"
    detector = ObjectDetection()
    detector.process_images(input_dir, output_file)
