#!/usr/bin/env python3

import json

data = ' {"base_waist_joint":0,"waist_link1_joint":0,"link1_link2_joint":30,"right_gripper_joint":0} '

joint_angles = json.loads(data)


print(f"Jointangles = {joint_angles}\n")


def assign_values(joint_angles:dict):
    base_waist_joint = 1.250
    waist_link1_joint = 1.001
    link1_link2_joint = 1.245
    right_gripper_joint = 0.122

    joint_angles["base_waist_joint"]= base_waist_joint
    joint_angles["waist_link1_joint"]= waist_link1_joint
    joint_angles["link1_link2_joint"]= link1_link2_joint
    joint_angles["right_gripper_joint"]= right_gripper_joint
    
    return joint_angles
    

print(f"Jointangles = {assign_values(joint_angles)}\n")