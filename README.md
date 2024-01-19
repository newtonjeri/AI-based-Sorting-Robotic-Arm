# AI-Based Sorting Robot Arm

## Overview

The AI-Based Sorting Robot Arm project integrates artificial intelligence with ROS2 (Robot Operating System 2) to create a robotic arm capable of efficient object detection, recognition, and sorting. The system employs a camera for visual input, allowing precise positioning of objects relative to the robot's base frame. The inverse kinematics are computed, and the solutions are sent to an Arduino via serial communication. The Arduino actuates the motors to move the end effector to the desired position, facilitating the accurate placement of objects into designated containers.

## Features

- Object detection and recognition using cutting-edge AI algorithms.
- ROS2 integration for seamless robot control and coordination.
- Real-time camera feed processing for accurate object identification.
- Flexible sorting capabilities adaptable to various objects and scenarios.
- Efficient pick and place operations executed by the robotic manipulator.

## Dependencies

- ROS2 (Robot Operating System 2) Humble
- Gazebo Ignition Fortress
- Python (version 3.10.12)
- OpenCV (version 4.7.0.68)
- YOLO (for AI-based object detection)
- C++ Serial Library (libserial-dev)
- ikpy package for kinematics 

## Installation

1. **ROS2 Installation on Ubuntu 22.04:**
   [ROS2 Installation Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

2. **Gazebo Ignition Fortress:**
   [Gazebo Installation Guide](https://gazebosim.org/docs/fortress/install_ubuntu)

3. **OpenCV (version 4.7.0.68) using PIP:**
   ```bash
    pip install opencv-python==4.7.0.68
   ```

4. **YOLO (for AI-based object detection):**
   ```bash
    pip install ultralytics
   ```

5. **C++ Serial Library:**
   ```bash
    sudo apt-get install libserial-dev
   ```
6. **ros2 control:**
    ```bash
    sudo apt-get install ros-humble-ros2-control
    ```
7. **gazebo ros2 control:**
    ```bash
    sudo apt-get install ros-humble-gazebo-ros2-control
    ```
8. **ros2 controllers:**
    ```bash
    sudo apt-get install ros-humble-ros2-controllers
    ```
9. **xacro:**
    ```bash
    sudo apt-get install ros-humble-xacro
    ```
## Usage

Launch the packages in the following order:

1. Gazebo simulation and controllers:
   ```bash
   ros2 launch robotic_arm_description robot_arm_gazebo.launch.py
   ros2 launch robotic_arm_controllers robot_arm_controllers.launch.py
   ```

2. Recognition using simulation camera:
   ```bash
   ros2 launch robotic_arm_recognition robotic_arm_recognition_model.launch.py
   ```

   OR, if using a physical camera:
   ```bash
   ros2 launch robotic_arm_camera robot_arm_camera.launch.py
   ```
3. Transformation of the dynamic links (detected objects)
   ```bash
   ros2 launch robotic_arm_transforms transforms.launch.xml
   ```
4. Solving the IK problems and computing the forward kinematics
   ```bash
   ros2 launch robotic_arm_kinematics robotic_arm_kinematics.launch.py
   ```

All the packages can be launch using this single command
   - Simulation:
     ```bash
     ros2 launch robotic_arm_bringup sim_robotic_arm.launch.py
     ```
   - Real robot:
     ```bash
     ros2 launch robotic_arm_bringup real_robotic_arm.launch.py
     ```

**Note:** Launch each package in a separate terminal window after sourcing.

## Configuration

[Detail any configuration files or settings that need to be modified.]

## Contributing

Contributions are welcome! Please follow our [contribution guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the [License Name] License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

We express our gratitude to the following and resources that have played a pivotal role in the development and inspiration of our AI-Based Sorting Robot Arm project:

- **ikpy (Inverse Kinematics):**
  by Manceron, Pierre
  - *Repository:* [ikpy GitHub Repository](https://github.com/Phylliade/ikpy)

- **fusion2urdf-master:**
  by Toshinori Kitamura
  - *Repository:* [fusion2urdf-master GitHub Repository](https://github.com/syuntoku14/fusion2urdf)

- **Robotmania YouTube Channel:**
  - *Creator:* [Robotmania](https://www.youtube.com/@robotmania8896)
  - *Inspirational Content:* Valuable insights and tutorials related to robotics.

- **The Construct:**
  - *Resource:* [The Construct](http://www.theconstructsim.com/)
  - *Contribution:* Educational content and tools for robotics simulation.

These contributions have significantly enriched our project, providing essential knowledge, tools, and inspiration. We appreciate the dedication and expertise demonstrated by these individuals and resources in advancing the field of robotics.

*Note: The acknowledgment of these contributions is made with utmost respect and appreciation for their valuable work in the robotics community.*

## Contact

- Newton Kariuki: newtonkariuki1999@gmail.com
- Kevin Kipkorir
- Joseph Kuria
- Geoffrey Theuri
- Elizabeth Musanga
- Agnes Nyutu

## Additional Resources

Enhance your understanding and skills with the following resources related to our AI-Based Sorting Robot Arm project:

- **ROS2 Humble Documentation:**
  - *Documentation Link:* [ROS2 Humble Documentation](https://docs.ros.org/en/humble/index.html)

- **ROS2 Control Documentation:**
  - *Documentation Link:* [ROS2 Control Documentation](https://control.ros.org/master/index.html)

- **Robotics and ROS 2 - Learn by Doing! Manipulators, Udemy Course:**
  - *Course Link:* [Udemy Robotics and ROS 2 Course](https://www.udemy.com/course/robotics-and-ros-2-learn-by-doing-manipulators/learn/lecture/37574372#overview)

- **Simulation Camera Tutorial:**
  - *Video Tutorial:* [Simulation Camera Tutorial on YouTube](https://www.youtube.com/watch?v=XqibXP4lwgA)

Explore these resources to delve deeper into ROS2, control systems, and gain practical insights into manipulators. The Udemy course offers hands-on learning, while the official ROS documentation provides comprehensive guides. Additionally, the simulation camera tutorial on YouTube can be a valuable visual aid in understanding simulation setups.

Feel free to leverage these resources to enhance your knowledge and proficiency in the field of robotics and ROS2.

*Note: The provided links are accurate as of the last update, and users are encouraged to verify the links for the latest information.*

