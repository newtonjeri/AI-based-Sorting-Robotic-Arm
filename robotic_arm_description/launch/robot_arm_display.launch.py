import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

package_name = "robotic_arm_description"

def generate_launch_description():
    robotic_arm_description_dir = get_package_share_directory('robotic_arm_description')

    DeclareLaunchArgument('rviz_config', 
                            default_value=os.path.join(
                                            robotic_arm_description_dir, 'rviz_configs', 'rviz_sim.rviz'
                                            ),
                            description='Absolute path to robot rviz config file')

    model_arg = DeclareLaunchArgument(name='model', 
                                      default_value=os.path.join(
                                                    robotic_arm_description_dir, 'urdf', 'robotic_arm.xacro'
                                                    ),
                                      description='Absolute path to robot urdf file')
    


    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)


  

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    # Robot state publisher node
    robot_state_publisher = Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        parameters =[{"robot_description": robot_description}]
    )
    

    #RVIZ pnode.
    # Get the file path of the configuration file to load
    rviz_config_file = os.path.join(get_package_share_directory(package_name), "rviz_configs", "rviz_sim.rviz")

    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        )


    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        # joint_state_publisher_gui_node,
        rviz_node
    ])
