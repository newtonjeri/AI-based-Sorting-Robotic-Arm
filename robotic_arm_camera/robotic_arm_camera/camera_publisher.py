#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Guyueju (www.guyuehome.com)
@Description: ROS2 Topic Example - Publishing Image Topic
"""

import rclpy                        # ROS2 Python interface library
from rclpy.node import Node         # ROS2 Node class
from sensor_msgs.msg import Image   # Image message type
from cv_bridge import CvBridge      # ROS and OpenCV image conversion class
import cv2                          # OpenCV image processing library

"""
Create a publisher node
"""
class ImagePublisher(Node):

    def __init__(self, name):
        super().__init__(name)                                           # Initialize the ROS2 node parent class
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)  # Create a publisher object (message type, topic name, queue length)
        self.timer = self.create_timer(0.1, self.timer_callback)         # Create a timer (period in seconds, callback function to be executed at each timer event)
        self.cap = cv2.VideoCapture(0)                                   # Create a video capture object to drive the camera for image capture (camera device number)
        self.cv_bridge = CvBridge()                                      # Create an image conversion object for later converting OpenCV images to ROS image messages

        self.get_logger().info('Camera Node started')                 # Output log information indicating that the image topic has been published

    def timer_callback(self):
        ret, frame = self.cap.read()                                     # Read each frame of the image
        
        if ret == True:                                                  # If the image is successfully read
            self.publisher_.publish(
                self.cv_bridge.cv2_to_imgmsg(frame, 'bgr8'))             # Publish the image message


def main(args=None):                                 # ROS2 node main entry point main function
    rclpy.init(args=args)                            # Initialize the ROS2 Python interface
    node = ImagePublisher("topic_webcam_pub")        # Create a ROS2 node object and initialize it
    rclpy.spin(node)                                 # Loop and wait for ROS2 to exit
    node.destroy_node()                              # Destroy the node object
    rclpy.shutdown()                                 # Close the ROS2 Python interface
