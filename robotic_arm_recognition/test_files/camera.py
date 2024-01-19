#!/usr/bin/env python3
import cv2
import numpy as np
import cv2.aruco as aruco
import cvzone
import math
import time
from ultralytics import YOLO

import os
from ament_index_python.packages import get_package_share_directory

def detect_aruco_and_get_reference_center(frame, aruco_dict, aruco_marker_size_mm, camera_matrix, dist_coeffs):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dictionary = aruco.getPredefinedDictionary(aruco_dict)
    parameters = aruco.DetectorParameters()
    # Detect markers
    markerCorners, markerIds, _ = aruco.detectMarkers(gray, dictionary, parameters=parameters)

    reference_center = None
    pixel_to_mm_ratio = None
    centers = {}

    if markerCorners and markerIds is not None:
        
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(markerCorners, aruco_marker_size_mm, camera_matrix, dist_coeffs)
        for idx, corners in enumerate(markerCorners):
            int_corners = np.int0(corners)
            center = np.mean(int_corners[0], axis=0)
            centers[int(markerIds[idx])] = center
            if markerIds[idx] == 1:
                reference_center = center
                aruco_side_pixels = np.linalg.norm(int_corners[0][0] - int_corners[0][1])
                pixel_to_mm_ratio = aruco_marker_size_mm / aruco_side_pixels

            # Draw axis for each marker
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[idx], tvecs[idx], aruco_marker_size_mm / 2)

    aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
    return reference_center, pixel_to_mm_ratio, centers

def resize_frame(frame, target_width=1366, target_height=768):
    height, width = frame.shape[:2]
    if width > target_width or height > target_height:
        scaling_factor = min(target_width / width, target_height / height)
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return frame

# Function to recognize object and position it with reference to the ArUco marker
def recognize_and_position_object():
    cap = cv2.VideoCapture(0)
   

    # Set the window size to fit your screen resolution
    window_width = 1366
    window_height = 768
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  # Create a resizable window
    cv2.resizeWindow("Image", window_width, window_height)
    location_path = os.path.join(get_package_share_directory("robotic_arm_recognition"), "test_files", "trained_model.pt")

    model = YOLO(location_path)
    classNames = ['Black-A', 'Red-A', 'Green-A', 'Cube', 'Hexagon', 'Cylinder']

    aruco_dict_type = aruco.DICT_4X4_50
    aruco_marker_size_mm = 34

    camera_matrix = np.array([[650, 0, 320], [0, 650, 240], [0, 0, 1]], dtype=np.float32)
    dist_coeffs = np.zeros((4,1), dtype=np.float32) 

    last_print_time = time.time()

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        reference_center, pixel_to_mm_ratio, aruco_centers = detect_aruco_and_get_reference_center(img, aruco_dict_type, aruco_marker_size_mm, camera_matrix, dist_coeffs)

        if reference_center is not None and pixel_to_mm_ratio is not None:
            results = model(img, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
                    relative_x, relative_y = center_x - reference_center[0], center_y - reference_center[1]
                    relative_x_cm, relative_y_cm = round(relative_x * pixel_to_mm_ratio / 10, 1), round(relative_y * pixel_to_mm_ratio / 10, 1)

                    cls = int(box.cls[0])
                    currentClass = classNames[cls]
                    myColor = (0, 0, 255) if cls < len(classNames) - 1 else (0, 255, 0)

                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 2)
                    cv2.putText(img, currentClass, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, myColor, 2)
                    cv2.putText(img, f'({relative_x_cm} cm, {relative_y_cm} cm)', (x1, y2 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, myColor, 2)

                    if time.time() - last_print_time >= 10:
                        print(f"Detected {currentClass}: Relative Position ({relative_x_cm} cm, {relative_y_cm} cm)")

        if time.time() - last_print_time >= 10:
            for markerId, center in aruco_centers.items():
                if markerId != 1:
                    relative_x, relative_y = center - reference_center
                    relative_x_cm, relative_y_cm = round(relative_x * pixel_to_mm_ratio / 10), round(relative_y * pixel_to_mm_ratio / 10)
                    print(f"ArUco Marker ID {markerId}: Relative Position ({relative_x_cm} cm, {relative_y_cm} cm)")

            last_print_time = time.time()

        img = resize_frame(img)  # Resize the frame before displaying
        cv2.imshow('Detection', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




def main():
    recognize_and_position_object()

if __name__ == "__main__":
    main()
