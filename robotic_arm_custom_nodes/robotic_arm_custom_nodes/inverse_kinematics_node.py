#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory , JointTrajectoryPoint
import ikpy.chain
import sys 
import numpy as np
import os
from ament_index_python.packages import get_package_share_directory

class Trajectory_publisher(Node):
    def __init__(self):
        # trajectory publisher node
        super().__init__('ik_node')
        # Topic to publish to
        publish_topic = "/robotic_arm_joint_trajectory_controller/joint_trajectory"
        # Creating the trajectory publisher
        self.trajectory_publisher = self.create_publisher(JointTrajectory, publish_topic, 10)
        timer_period = 1.0
        # Creating a timer
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Joints to be controlled
        self.joints = [ "base_waist_joint",
                        "waist_link1_joint",
                        "link1_link2_joint",
                        "link2_gripper_base_joint",
                        "right_gripper_joint"
                        ]


        # URDF file of the robot
        urdf_file = os.path.join(get_package_share_directory("robotic_arm_description"), "urdf", "robotic_arm_urdf.urdf")  
        
        ## Toolbox interface
        self.robot_initialize(urdf_file)
        argv = sys.argv[1:] 
        self.inverse_kinematics_solution(float(argv[0]),float(argv[1]),float(argv[2]))
    
    # Timer callback function
    def timer_callback(self):
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = self.joints
        point = JointTrajectoryPoint()
        point.positions = self.goal_positions
        point.time_from_start = Duration(sec=2)
        trajectory_msg.points.append(point)
        self.trajectory_publisher.publish(trajectory_msg)
        print("\nTrajectory Sent !\n")

    # Function to initialize urdf
    def robot_initialize(self,urdf_file):
        self.robotic_arm = ikpy.chain.Chain.from_urdf_file(urdf_file, active_links_mask=[False, False, True, True, True, True, False])
    
    # Forward Kinematics Solver
    def get_fk_solution(self):
        T=self.robotic_arm.forward_kinematics([0] * 7)
        print("\nTransformation Matrix :\n",format(T))
    
    # Inverse Kinematics Solver
    def inverse_kinematics_solution(self,x,y,z):
        angles=self.robotic_arm.inverse_kinematics([x,y,z])
        angles = np.delete(angles, [0, 1, 6])
        angles = np.append(angles, 0.0)
        self.goal_positions = list(angles) 
       
        print("\nInverse Kinematics Solution :\n" ,self.goal_positions)



def main(args=None):
    # initialize ros2 communication
    rclpy.init(args=args)
    # Creating a Trajectory_publisher object
    joint_trajectory_object = Trajectory_publisher()

    # Spinning the node
    rclpy.spin(joint_trajectory_object)
    # Killing the node
    joint_trajectory_object.destroy_node()
    # Stoping ros2 communication
    rclpy.shutdown()

if __name__ == '__main__':
    main()