
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="robotic_arm_camera",
            executable="camera_publisher",
            name="camera_publisher",
            output="screen",
        ),
        Node(
            package="robotic_arm_camera",
            executable="camera_subscriber",
            name="camera_subscriber",
            output="screen",
        ),
    ])