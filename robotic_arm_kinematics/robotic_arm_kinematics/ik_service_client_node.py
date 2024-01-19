#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from numpy import pi
from robotic_arm_msgs.srv import IKSolver
from robotic_arm_msgs.msg import WorldObjectInference
import time
from functools import partial

DELAY = 5
TRAJECTORY_HEIGHT = 200


class IKClientNode(Node):
    def __init__(self):
        super().__init__('ik_client_node')
        
        # Object pos, for testing, tobe removed
        self.object_position = [190, -190, 100]
 
        # List to store previous detected objects and their positions in the scene
        self.previous_positions = []
    
        # Z Position of the gripper when placing an object
        self.placing_coord_z = 200

        # Robot's home position
        self.home_pos = [13, -241, 292]

        # List to store positions of the cylinders, cubes, and hexagons containers respectively
        self.cylinders_container_pos = [-242, 20, self.placing_coord_z]
        self.cubes_container_pos = [-150, -230, self.placing_coord_z]
        self.hexagons_container_pos = [ -150, 20, self.placing_coord_z]

        # Gripper States and their corresponding angles
        self.GRIPPER_OPEN = pi/3
        self.GRIPPER_CLOSE = pi/6

        # List to store the variable of where the object picked and is to be placed
        self.start_position = self.home_pos
        self.end_position = self.hexagons_container_pos

        # Subscriber to the worldObjectInference topic
        self.pos_subscriber = self.create_subscription(
            WorldObjectInference,
            '/world_object_inference',
            self.object_inference_callback,
            10)

        
        # self.timer = self.create_timer(5.0, self.timer_callback)
        

    def timer_callback(self):
        self.pick_and_place_object()
        self.get_logger().info("Ready to kill timer")
        self.timer.cancel()


    # Service client setup
    def service_client_setup(self, x, y, z, gripper_state):
        # Service client to the IK solver service
        self.client_ = self.create_client(IKSolver, 'ik_server')
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('service not available, waiting again...')

        self.request = IKSolver.Request()
        self.request.x_coord = x
        self.request.y_coord = y
        self.request.z_coord = z
        self.request.gripper_state = gripper_state

        self.future_ = self.client_.call_async(self.request)
        self.future_ = self.future_.add_done_callback(partial(self.response_callback))


    # Callback function for the subscriber
    def object_inference_callback(self, msg):
        class_names = msg.class_names
        object_positions = msg.detected_obj_positions

        # Construct a list of lists from the class names and object positions
        objects_and_positions = self.construct_2d_list(class_names, object_positions)
        

        self.get_logger().info(f"Received class names: {class_names}")
        self.get_logger().info(f"Received object positions: {objects_and_positions}")
        self.get_logger().info(f"Previous object positions: {self.previous_positions}")

        # If the object positions are the same as the previous positions, do nothing 
        if  self.compare_lists(objects_and_positions, self.previous_positions) == True:
            self.get_logger().info("No new objects detected")
        elif self.compare_lists(objects_and_positions, self.previous_positions) == False:
            self.get_logger().info("Object positions changed")
            self.previous_positions = objects_and_positions
            object_to_pick = self.first_object_to_pick_determiner(self.previous_positions)
            class_name = object_to_pick[0]
            x = int(object_to_pick[1])
            y = int(object_to_pick[2])
            z = int(object_to_pick[3])

            self.object_position = [x, y, z]

            # Determine the end position based on the class name
            if class_name == "Cylinder":
                self.end_position = self.cylinders_container_pos
            elif class_name == "Cube":
                self.end_position = self.cubes_container_pos
            elif class_name == "Hexagon":
                self.end_position = self.hexagons_container_pos
            else:
                self.end_position = self.home_pos

            # Remove the object from the list
            self.previous_positions.pop(self.previous_positions.index(object_to_pick))
            
            # Pick and place the object
            self.pick_and_place_object()
        else:
            self.get_logger().warn("No Object to Pick")


    # Callback function for the service client
    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Received joint angles: {response.joint_angles}")
        except Exception as e:
            self.get_logger().error(f"Service call failed {e}")


    # Function to open and close the gripper
    def open_close_gripper(self, gripper_state: bool):
        if gripper_state == True:
            print("Opening gripper")
            return self.GRIPPER_OPEN
        else:
            print("Closing gripper")
            return self.GRIPPER_CLOSE
        

    # Function to decide what Object to pick first
    def first_object_to_pick_determiner(self, objects_list):
        if len(objects_list) == 0:
            return None
        else:
            x_closest = objects_list[0][1]
            object_to_pick = objects_list[0]
            # Pick object closest to the robot's base position wrt x axis
            for object in range(len(objects_list)):
                if objects_list[object][1] < x_closest:
                    x_closest = objects_list[object][1]
                    object_to_pick = objects_list[object]

        return object_to_pick
            
    # Define the pick and place logic
    def pick_and_place_object(self):
        # Open gripper
        self.service_client_setup(self.home_pos[0], self.home_pos[1], self.home_pos[2], True)
        time.sleep(DELAY)
        # Move to the object's position
        self.service_client_setup(self.object_position[0], self.object_position[1], TRAJECTORY_HEIGHT, True)
        time.sleep(DELAY)
        # Close the gripper
        self.service_client_setup(self.object_position[0], self.object_position[1], self.object_position[2], True)
        time.sleep(DELAY)
        # Close the gripper
        self.service_client_setup(self.object_position[0], self.object_position[1], self.object_position[2], False)
        time.sleep(DELAY)
        # Move to trajectory height to avoid collisiom
        self.service_client_setup(self.object_position[0], self.object_position[1], TRAJECTORY_HEIGHT, False)
        time.sleep(DELAY)
        # Move to the placing position
        self.service_client_setup(self.end_position[0], self.end_position[1], self.end_position[2], False)
        time.sleep(DELAY)
        # Dropping the object
        self.service_client_setup(self.end_position[0], self.end_position[1], self.end_position[2], True)
        time.sleep(DELAY)
        # Open the gripper
        self.service_client_setup(self.end_position[0], self.end_position[1], self.end_position[2], False)
        time.sleep(DELAY)
        # Return to home position
        self.service_client_setup(self.home_pos[0], self.home_pos[1], self.home_pos[2], False)
        time.sleep(DELAY)


    # Function to compare two lists
    def compare_lists(self, list1, list2):
        # List1 and list2 are lists of lists
        # If the lists are of the same length, compare the elements
        if len(list1) == 0:
            return None
        else:
            if len(list1) != len(list2):
                return False
            else:
                # If the lists are of the same length, compare the first elements of each list
                for i in range(len(list1)):
                    if list1[i][0] != list2[i][0]:
                        return False
                    else:
                        continue
                
            return True
        
            

    # Function to construct a list of lists from 2 lists
    def construct_2d_list(self, list1, list2):
        list_of_lists = []

        for i in range(len(list1)):
            list_of_lists.append([list1[i], list2[i * 3], list2[i * 3 + 1], list2[i * 3 + 2]])

        return list_of_lists
    
    


def main():
    rclpy.init(args=None)
    ik_client_node = IKClientNode()
    rclpy.spin(ik_client_node)
    ik_client_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()