#!/usr/bin/env python3

import cv2
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from ultralytics import YOLO
import numpy as np
import cv2.aruco as aruco
import time

import os
from ament_index_python.packages import get_package_share_directory

class ObjectRecognitionNode(Node):
    def __init__(self):
        super().__init__('object_recognition_node')
        location_path = os.path.join(get_package_share_directory("robotic_arm_recognition"), "test_files", "trained_model.pt")

        
        self.declare_parameters(
            namespace='',
            parameters=[
                ('model_path', location_path),
            ]
        )

        

        self.model = YOLO(self.get_parameter('model_path').value)

        self.bridge = CvBridge()
        self.image_subscriber = self.create_subscription(Image, 'image', self.image_callback, 10)

        self.object_publisher = self.create_publisher(String, 'detected_object', 10)
        self.relative_position_publisher = self.create_publisher(Float32, 'relative_position', 10)

        self.aruco_dict_type = aruco.DICT_4X4_50
        self.aruco_marker_size_mm = 34

        self.camera_matrix = np.array([[650, 0, 320], [0, 650, 240], [0, 0, 1]], dtype=np.float32)
        self.dist_coeffs = np.zeros((4, 1), dtype=np.float32)

        self.last_print_time = time.time()

        self.cap = cv2.VideoCapture(0)  # 0 indicates the default webcam, change if you have multiple cameras

        if not self.cap.isOpened():
            self.get_logger().error("Error: Couldn't open the webcam.")
            rclpy.shutdown()

    def main_loop(self):
        while rclpy.ok():
            ret, img = self.cap.read()
            if not ret:
                self.get_logger().error("Failed to grab frame")
                break

            reference_center, pixel_to_mm_ratio, aruco_centers = self.detect_aruco_and_get_reference_center(img)

            if reference_center is not None and pixel_to_mm_ratio is not None:
                self.recognize_and_position_object()

            rclpy.spin_once(self)


    def detect_aruco_and_get_reference_center(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dictionary = aruco.getPredefinedDictionary(self.aruco_dict_type)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(dictionary, parameters)
        markerCorners, markerIds, _ = detector.detectMarkers(frame)

        reference_center = None
        pixel_to_mm_ratio = None
        centers = {}

        if markerCorners and markerIds is not None:
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(markerCorners, self.aruco_marker_size_mm,
                                                             self.camera_matrix, self.dist_coeffs)
            for idx, corners in enumerate(markerCorners):
                int_corners = np.int0(corners)
                center = np.mean(int_corners[0], axis=0)
                centers[int(markerIds[idx])] = center
                if markerIds[idx] == 1:
                    reference_center = center
                    aruco_side_pixels = np.linalg.norm(int_corners[0][0] - int_corners[0][1])
                    pixel_to_mm_ratio = self.aruco_marker_size_mm / aruco_side_pixels

                cv2.drawFrameAxes(frame, self.camera_matrix, self.dist_coeffs, rvecs[idx], tvecs[idx],
                                  self.aruco_marker_size_mm / 2)

        aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
        return reference_center, pixel_to_mm_ratio, centers

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        reference_center, pixel_to_mm_ratio, aruco_centers = self.detect_aruco_and_get_reference_center(frame)

        if reference_center is not None and pixel_to_mm_ratio is not None:
            results = self.model(frame, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
                    relative_x, relative_y = center_x - reference_center[0], center_y - reference_center[1]
                    relative_x_cm, relative_y_cm = round(relative_x * pixel_to_mm_ratio / 10, 1), round(
                        relative_y * pixel_to_mm_ratio / 10, 1)

                    cls = int(box.cls[0])
                    currentClass = self.get_class_name(cls)
                    myColor = (0, 0, 255) if cls < len(self.model.names) - 1 else (0, 255, 0)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), myColor, 2)
                    cv2.putText(frame, currentClass, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, myColor, 2)
                    cv2.putText(frame, f'({relative_x_cm} cm, {relative_y_cm} cm)', (x1, y2 + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, myColor, 2)

                    if time.time() - self.last_print_time >= 10:
                        print(f"Detected {currentClass}: Relative Position ({relative_x_cm} cm, {relative_y_cm} cm)")

            if time.time() - self.last_print_time >= 10:
                for markerId, center in aruco_centers.items():
                    if markerId != 1:
                        relative_x, relative_y = center - reference_center
                        relative_x_cm, relative_y_cm = round(relative_x * pixel_to_mm_ratio / 10), round(
                            relative_y * pixel_to_mm_ratio / 10)
                        print(f"ArUco Marker ID {markerId}: Relative Position ({relative_x_cm} cm, {relative_y_cm} cm)")

                self.last_print_time = time.time()

            self.object_publisher.publish(self.get_detected_object_msg())
            self.relative_position_publisher.publish(self.get_relative_position_msg(relative_x_cm, relative_y_cm))

            frame = self.resize_frame(frame)  # Resize the frame before displaying
            cv2.imshow('Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.destroy_node()
                rclpy.shutdown()

    def get_class_name(self, class_id):
        if class_id < len(self.model.names):
            return self.model.names[class_id]
        return "Unknown"

    def get_detected_object_msg(self):
        msg = String()
        msg.data = "Detected Object"
        return msg

    def get_relative_position_msg(self, relative_x_cm, relative_y_cm):
        msg = Float32()
        msg.data = relative_x_cm + relative_y_cm  # You might want to customize this based on your needs
        return msg

    def resize_frame(self, frame, target_width=1366, target_height=768):
        height, width = frame.shape[:2]
        if width > target_width or height > target_height:
            scaling_factor = min(target_width / width, target_height / height)
            frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        return frame


def main(args=None):
    rclpy.init(args=args)
    node = ObjectRecognitionNode()
    node.main_loop()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
