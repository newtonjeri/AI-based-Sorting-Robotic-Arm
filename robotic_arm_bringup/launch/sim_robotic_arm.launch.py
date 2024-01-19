import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    gazebo = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("robotic_arm_description"),
                "launch",
                "robot_arm_gazebo.launch.py"
            )
        )
    
    controllers = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("robotic_arm_controllers"),
                "launch",
                "robot_arm_controllers.launch.py"
            ),
            launch_arguments={"sim_mode": "True"}.items()
        )
    
    rviz = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robotic_arm_description"),
            "launch",
            "robot_arm_display.launch.py"
        ),
        launch_arguments={"sim_mode": "True"}.items()
    )
    
    
    sim_camera = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robotic_arm_recognition"),
            "launch",
            "robotic_arm_recognition_model.launch.py"
        )
    )
    
    transforms = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("robotic_arm_transforms"),
                "launch",
                "transforms.launch.xml"
            )
    )
    
    kinematics = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("robotic_arm_kinematics"),
                "launch",
                "robotic_arm_kinematics.launch.py"
            ),
        )
    
    return LaunchDescription([
        rviz,
        gazebo,
        controllers,
        sim_camera,
        kinematics,
        transforms
    ])