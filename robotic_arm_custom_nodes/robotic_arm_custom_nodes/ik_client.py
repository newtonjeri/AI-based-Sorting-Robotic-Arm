#! /usr/bin/env python3

"""
Client node
"""

import rclpy
from rclpy.node import Node
from numpy import pi
from robotic_arm_msgs.srv import IKSolver


class IKClient(Node):
    def __init__(self):
        super().__init__("ik_client")
        self.client = self.create_client(IKSolver, "ik_solution")

        # Wait for service serve to be active
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for server...")
        
        




def main(args=None):
    rclpy.init(args=args)
    node = IKClient()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()