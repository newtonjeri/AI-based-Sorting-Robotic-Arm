cmake_minimum_required(VERSION 3.8)
project(robotic_arm_kinematics)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)

# Include cpp "include" directory
include_directories(include)

# Create c++ executables
# add_executable(exec_name src/file.cpp src/file2.cpp)
# ament_target_dependencies(exec_name rclcpp std_msgs)

# install cpp executables
# install(
#   exec_name
#   DEFINITION lib/${PROJECT_NAME}
# )

install(
  DIRECTORY
    ${PROJECT_NAME}
    launch
  DESTINATION
    share/${PROJECT_NAME}/
)

# install Python executables
install(
  PROGRAMS
    ${PROJECT_NAME}/ik_service_server_node.py
    ${PROJECT_NAME}/ik_service_client_node.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
