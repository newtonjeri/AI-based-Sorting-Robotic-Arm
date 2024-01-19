
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="robotic_arm_kinematics",
            executable="ik_service_server_node.py",
            name="ik_server_node",
            output="screen",
            emulate_tty=True,
        ),
        Node(
            package="robotic_arm_kinematics",
            executable="ik_service_client_node.py",
            name="ik_client_node",
            output="screen",
            emulate_tty=True,
        ),
    ])