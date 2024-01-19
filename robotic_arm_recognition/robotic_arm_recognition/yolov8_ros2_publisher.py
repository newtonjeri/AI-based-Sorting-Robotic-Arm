#!/usr/bin/env python3

from ultralytics import YOLO
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2.aruco as aruco
import cv2
import numpy as np
from ament_index_python.packages import get_package_share_directory
import os

from robotic_arm_msgs.msg import ObjectInference
from robotic_arm_msgs.msg import Yolov8Inference


# Define the picking height of the robotic arm
PICKING_HEIGHT = 50

# Define the x-axis drift of the robotic arm
ARUCO_MARKER_SIZE_MM = 34
Y_DRIFT = 300 - int(ARUCO_MARKER_SIZE_MM / 2)

class Camera_subscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')

        self.cv2_bridge = CvBridge()

        self.aruco_dict_type = aruco.DICT_4X4_50                # Define the ArUco marker dictionary type
        self.aruco_marker_size_mm = ARUCO_MARKER_SIZE_MM   
        location_path = os.path.join(get_package_share_directory("robotic_arm_recognition"), "Computer_Vision_Models", "5best.pt")

        self.model = YOLO(location_path)

        self.yolov8_inference = Yolov8Inference()
        self.object_inference = ObjectInference()

        self.camera_matrix = np.array([[650, 0, 320], [0, 650, 240], [0, 0, 1]], dtype=np.float32)
        self.dist_coeffs = np.zeros((4, 1), dtype=np.float32)

        self.subscription = self.create_subscription(
            Image,
            'rgb_cam/image_raw',
            self.camera_call_back,
            10)
        

        self.yolov8_pub = self.create_publisher(Yolov8Inference, "/Yolov8_Inference", 1)
        self.img_pub = self.create_publisher(Image, "/object_inference", 1)

    def camera_callback(self, data):
        img = self.cv2_bridge.imgmsg_to_cv2(data, "bgr8")

        results = self.model(img)

        for r in results:
            boxes = r.boxes
            for box in boxes:

                b = box.xyxy[0].to('cpu').detach().numpy().copy()  # get box coordinates in (top, left, bottom, right) format
                c = box.cls
                x_center: int = int(((b[0] + b[2]) / 2))
                y_center: int = int(((b[1] + b[3]) / 2))
                self.object_inference.class_name = self.model.names[int(c)]
                self.object_inference.x_coord = x_center
                self.object_inference.y_coord = y_center
                self.object_inference.z_coord = PICKING_HEIGHT

                if self.object_inference.class_name == "Cylinder" or self.object_inference.class_name == "Cube" or self.object_inference.class_name == "Hexagon":
                    self.yolov8_inference.class_names.append(self.object_inference.class_name)
                    self.yolov8_inference.detected_obj_positions.append(str(self.object_inference.x_coord))
                    self.yolov8_inference.detected_obj_positions.append(str(self.object_inference.y_coord))
                    self.yolov8_inference.detected_obj_positions.append(str(self.object_inference.z_coord))

        annotated_frame = results[0].plot()
        img_msg = self.cv2_bridge.cv2_to_imgmsg(annotated_frame)  

        self.img_pub.publish(img_msg)
        self.yolov8_pub.publish(self.yolov8_inference)
        self.yolov8_inference.class_names.clear()
        self.yolov8_inference.detected_obj_positions.clear()


    # Detect the ArUco marker and get the reference center
    def detect_aruco_and_get_reference_center(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dictionary = aruco.getPredefinedDictionary(self.aruco_dict_type)
        parameters = aruco.DetectorParameters()
        markerCorners, markerIds, _ = aruco.detectMarkers(gray, dictionary, parameters=parameters)

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

    # Function to detect and position aobjects    
    def detect_and_position_object(self, image):
        reference_center, pixel_to_mm_ratio, aruco_centers = self.detect_aruco_and_get_reference_center(image)

        results = self.model(image)

        if reference_center is not None and pixel_to_mm_ratio is not None:
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    self.object_inference = ObjectInference()

                    # Coordinates of the bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])    
                    # Class of the detected object     
                    c = box.cls

                    # x_origin, y_origin, aruco
                    x_origin = reference_center[1] * pixel_to_mm_ratio
                    y_origin = reference_center[0] * pixel_to_mm_ratio

                    # x_origin, y_origin = self.transform_aruco_center_to_robot_base(Y_DRIFT, x_origin, y_origin)

                    # Calculate the centres of the bounding box
                    x_center = (x1 + x2) / 2
                    y_center = (y1 + y2) / 2

                    x_center = x_center * pixel_to_mm_ratio
                    y_center = y_center * pixel_to_mm_ratio

                    x_pos = int(x_center - x_origin)
                    y_pos = int(y_center - y_origin)
                    

                    self.object_inference.class_name = self.model.names[int(c)]
                    self.object_inference.x_coord = x_pos
                    self.object_inference.y_coord = y_pos
                    self.object_inference.z_coord = PICKING_HEIGHT

                    if self.object_inference.class_name == "Cylinder" or self.object_inference.class_name == "Cube" or self.object_inference.class_name == "Hexagon":
                        self.yolov8_inference.class_names.append(self.object_inference.class_name)
                        self.yolov8_inference.detected_obj_positions.append(str(self.object_inference.x_coord))
                        self.yolov8_inference.detected_obj_positions.append(str(self.object_inference.y_coord))
                        self.yolov8_inference.detected_obj_positions.append(str(self.object_inference.z_coord))

                        cls = int(c)
                        currentClass = self.object_inference.class_name
                        myColor = (0, 0, 255) if cls < len(self.model.names) - 1 else (0, 255, 0)
                        cv2.putText(image, currentClass, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, myColor, 2)
                        cv2.putText(image, f'({x_pos} mm, {y_pos} mm)', (x1, y1 + int(2 * y_center - 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, myColor, 2)

            annotated_frame = results[0].plot()
            img_msg = self.cv2_bridge.cv2_to_imgmsg(annotated_frame)  

            self.img_pub.publish(img_msg)
            self.yolov8_pub.publish(self.yolov8_inference)
            self.yolov8_inference.class_names.clear()
            self.yolov8_inference.detected_obj_positions.clear()
            # self.resize_frame(annotated_frame, 650, 350)
            # cv2.imshow("Object Recognition and Positioning", annotated_frame)                    # Display the image
            # cv2.waitKey(1)

    def camera_call_back(self, data):
        self.get_logger().info('Receiving video frame')         # Output log information indicating that the callback function has been entered
        image = self.cv2_bridge.imgmsg_to_cv2(data, 'bgr8')     # Convert the ROS image message to an OpenCV image
        self.detect_and_position_object(image)                  # Object detection and positioning


if __name__ == '__main__':
    rclpy.init(args=None)
    camera_subscriber = Camera_subscriber()
    rclpy.spin(camera_subscriber)
    rclpy.shutdown()