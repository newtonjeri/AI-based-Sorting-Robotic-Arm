from math import pi
from time import time

# Z Position of the gripper when picking up an object
picking_coord_z = 0.1   
# Z Position of the gripper when placing an object
placing_coord_z = 0.2

# Robot's home position
home_pos = [0.0, 0.0, 0.0]

# List to store positions of the cylinders, cubes, and hexagons containers respectively
cylinders_container_pos = [0.2, -0.2, 0.2]
cubes_container_pos = [0.1, 0.4 , 0.2]
hexagons_container_pos = [0.3, 0.5 , 0.2]

# Gripper States and their corresponding angles
GRIPPER_OPEN = pi/3
GRIPPER_CLOSE = 0

# List to store the data of objects recognized and positioned by camera
objects_list = [
                    ["Cylinder", 0.1, -0.2, picking_coord_z],
                    ["Cylinder", 0.2, -0.1, picking_coord_z],
                    ["Hexagon", 0.3, -0.1, picking_coord_z],
                    ["Hexagon", 0.3, -0.15, picking_coord_z],
                    ["Cube", 0.1, -0.1, picking_coord_z],
                    ["Cube", 0.1, -0.3, picking_coord_z]
                ]

# Function to decide what Object to pick first
def first_object_to_pick_determiner(objects_list):
    x_closest = objects_list[0][1]
    object_to_pick = objects_list[0]
    # Pick object closest to the robot's base position wrt x axis
    for object in range(len(objects_list)):
        if objects_list[object][1] < x_closest:
            x_closest = objects_list[object][1]
            object_to_pick = objects_list[object]

    # Remove the object from the list
    objects_list.remove(object_to_pick)
    return object_to_pick

# Function to generate the start (pick) position for a given object
def generate_picking_position(object: list):
    if object[0] == "Cylinder":
        print(f"Picking {object[0]} at x = {object[2]}, y = {object[3]}")
        return [0.0, 0.0, object[2]]
    elif object[0] == "Cube":
        print(f"Picking {object[0]} at x = {object[2]}, y = {object[3]}")
        return [0.0, 0.0, object[2]]
    elif object[0] == "Hexagon":
        print(f"Picking {object[0]} at x = {object[2]}, y = {object[3]}")
        return [0.0, 0.0, object[2]]
    else:
        print(f"Returning to home position")
        return home_pos
    

# Function to decide where to place the object picked based on its class name
def generate_placing_position(object: list):
    if object[0] == "Cylinder":
        print(f"Placing {object[0]} at {cylinders_container_pos}")
        return cylinders_container_pos
    elif object[0] == "Cube":
        print(f"Placing {object[0]} at {cubes_container_pos}")
        return cubes_container_pos
    elif object[0] == "Hexagon":
        print(f"Placing {object[0]} at {hexagons_container_pos}")
        return hexagons_container_pos
    else:
        print(f"Returning to home position")
        return home_pos

# Function to open and close the gripper
def open_close_gripper(gripper_state: bool):
    if gripper_state == True:
        print("Opening gripper")
        return GRIPPER_OPEN
    else:
        print("Closing gripper")
        return GRIPPER_CLOSE

def main():
    # Simulating the pick and place logic
    for i in range(len(objects_list)):
        print(f"Picking and placing object number {i+1}")
        object_to_pick = first_object_to_pick_determiner(objects_list)
        generate_picking_position(object_to_pick)
        print(f"Moving object number {i+1} to the {object_to_pick[0]} container")
        generate_placing_position(object_to_pick)
        open_close_gripper(True)
        open_close_gripper(False)
        generate_picking_position(home_pos)
        print("\n")
    print("All objects have been picked and placed")
        


if __name__ == "__main__":
    main()
