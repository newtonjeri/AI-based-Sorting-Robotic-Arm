#!/usr/bin/env python3

import os
import numpy as np
import rclpy
import ikpy.chain
from rclpy.node import Node
import serial, time

from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState

from ament_index_python.packages import get_package_share_directory

from robotic_arm_msgs.srv import IKSolver

HOME_POSITION = [np.pi/2, np.pi/2, np.pi/2, np.pi/2, 0.0]

# URDF file of the robot
urdf_file = os.path.join(get_package_share_directory("robotic_arm_description"), "urdf", "robotic_arm_urdf.urdf")  

class IKServerNode(Node):
    def __init__(self):
        super().__init__('ik_server_node')

        # Create a service server for finding the IK solution
        self.service_ = self.create_service(IKSolver, "ik_server", self.ik_solver_callback)
        self.get_logger().info("Starting IK Server Node")

        # Topic to publish to
        publish_topic = "/robotic_arm_joint_trajectory_controller/joint_trajectory"
        # Creating the trajectory publisher
        self.trajectory_publisher = self.create_publisher(JointTrajectory, publish_topic, 10)
        self.timer_period = 1.0
        #self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Goal Positions
        self.goal_positions = HOME_POSITION
        # Joints to be controlled
        self.joints = [ "base_waist_joint",
                        "waist_link1_joint",
                        "link1_link2_joint",
                        "link2_gripper_base_joint",
                        "right_gripper_joint"
                        ]
        

    # Callback function for the service
    def ik_solver_callback(self, request, response):
        self.get_logger().info(f"Received position x={request.x_coord} y={request.y_coord} z={request.z_coord}")
        response.joint_angles = self.inverse_kinematics_solution(request.x_coord/1000, request.y_coord/1000, request.z_coord/1000, request.gripper_state)
        # Creating a timer   
        arduino_data =  "a" + str(int(90 + np.rad2deg(response.joint_angles[0]))) \
                        + ",b" + str(int(90 - np.rad2deg(response.joint_angles[1]))) \
                        + ",c" + str(int(90 + np.rad2deg(response.joint_angles[2]))) \
                        + ",d" + str(int(90 - np.rad2deg(response.joint_angles[3]))) \
                        + ",e" + str(int(np.rad2deg(response.joint_angles[4]))) + ",\n"

        #arduino_data = "a90,b90,c90,d0,e60,\n"
        #######################################################

        self.get_logger().info(f"Data Sent to arduino = {arduino_data}")

        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = self.joints
        point = JointTrajectoryPoint()
        point.positions = self.goal_positions
        point.time_from_start = Duration(sec=2)
        trajectory_msg.points.append(point)
        self.trajectory_publisher.publish(trajectory_msg)
        self.send_to_arduino(arduino_data)

        self.get_logger().info(f"IK solution: {response.joint_angles}")
        return response

    # JTC publisher callback function
    def timer_callback(self):
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = self.joints
        point = JointTrajectoryPoint()
        point.positions = self.goal_positions
        point.time_from_start = Duration(sec=2)
        trajectory_msg.points.append(point)
        self.trajectory_publisher.publish(trajectory_msg)
        self.get_logger().info(f"Timer Goal Positions = {self.goal_positions}")
    
    
    # Function to initialize urdf
    def robot_initialize(self,urdf_file):
        self.robotic_arm = ikpy.chain.Chain.from_urdf_file(urdf_file, active_links_mask=[False, False, True, True, True, True, False])
    

    # Forward Kinematics Solver
    def get_fk_solution(self):
        self.robot_initialize(urdf_file)
        T=self.robotic_arm.forward_kinematics([0] * 7)
        print("\nTransformation Matrix :\n",format(T))
        return T


    # Inverse Kinematics Solver
    def inverse_kinematics_solution(self,x,y,z, gripper):
        self.robot_initialize(urdf_file)
        angles=self.robotic_arm.inverse_kinematics([x,y,z])
        angles = np.delete(angles, [0, 1, 6])
        if gripper:
            angles = np.append(angles, [np.pi/3])
        else:
            angles = np.append(angles, [0])

        self.goal_positions = list(angles) 
        print("\nInverse Kinematics Solution :\n" ,self.goal_positions)
        return self.goal_positions
    
    # Function to send data to Arduino
    def send_to_arduino(self, data: str):
        try:
            # Serial port setup
            self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
            self.ser.flush()
            self.ser.write(data.encode('utf-8'))
            self.get_logger().info("Sent to Arduino: " + data)


        except serial.SerialException as e:
            self.get_logger().error(f"Could not send data due to this error: {e}")


# Main function
def main():
    rclpy.init(args=None)
    ik_server_node = IKServerNode()
    rclpy.spin(ik_server_node)
    ik_server_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()