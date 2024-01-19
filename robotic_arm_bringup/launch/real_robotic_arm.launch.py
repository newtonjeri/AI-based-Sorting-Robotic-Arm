import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    controllers = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("robotic_arm_controllers"),
                "launch",
                "robot_arm_controllers.launch.py"
            ),
            launch_arguments={"sim_mode": "False"}.items()
        )
    
    rviz = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("robotic_arm_description"),
                "launch",
                "robot_arm_display.launch.py"
            ),
            launch_arguments={"sim_mode": "False"}.items()
        )

    
    return LaunchDescription([
        controllers,
        rviz,
    ])