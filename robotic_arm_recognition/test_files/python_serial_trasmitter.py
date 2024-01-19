#! /usr/bin/env python3

# Program to compare lists

# List to store previous detected objects and their positions in the scene
previous_positions = [" ", " ", " ", " "]
objects_positions = ["Cylinder", "0.533", "0.1111", "0.3333"]

# list of length 3
list1 = [1, 2, 3]

# list of length 9 of lettera
list2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


    # Function to construct a list of lists from 2 lists
def construct_2d_list(list1, list2):
    list_of_lists = []

    for i in range(len(list1)):
        list_of_lists.append([list1[i], list2[i * 3], list2[i * 3 + 1], list2[i * 3 + 2]])

    return list_of_lists

construct_2d_list = construct_2d_list(list1, list2)
print("Construct 2d list original: ", construct_2d_list)
item = construct_2d_list[1]
construct_2d_list.pop(construct_2d_list.index(item))
print("Construct 2d list modified : ", construct_2d_list)
