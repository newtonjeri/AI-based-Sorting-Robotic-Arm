# This is a python launch file that loads a URDF file and launches RViz
import os
import launch
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the path to the URDF file
    urdf_file_path = os.path.join(
        get_package_share_directory('robotic_arm_description'),
        'urdf',
        'robotic_arm_urdf.urdf')

    # Load the URDF file as a parameter
    robot_description = open(urdf_file_path).read()

    # joint state publisher GUI node
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    # robot state publisher node
    robot_state_publisher = launch_ros.actions.Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        parameters =[{"robot_description": robot_description}]
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(get_package_share_directory('robotic_arm_description'), 'rviz', 'display.rviz')],
    )

    return launch.LaunchDescription([
        joint_state_publisher_gui_node,
        robot_state_publisher,
        rviz_node
    ])