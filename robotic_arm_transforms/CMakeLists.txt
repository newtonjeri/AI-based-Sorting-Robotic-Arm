cmake_minimum_required(VERSION 3.8)
project(robotic_arm_transforms)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp)
find_package(tf2_ros)
find_package(robotic_arm_msgs)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

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

add_executable(transformer src/apply_transfroms.cpp)#apply_transfroms.cpp
ament_target_dependencies(transformer rclcpp std_msgs tf2_ros robotic_arm_msgs)

add_executable(get src/get_transform.cpp)#apply_transfroms.cpp
ament_target_dependencies(get rclcpp std_msgs tf2_ros robotic_arm_msgs)

install(TARGETS
  transformer
  DESTINATION lib/${PROJECT_NAME}
  )

  install(TARGETS
    get
    DESTINATION lib/${PROJECT_NAME}
    )

    install(
    DIRECTORY launch
    DESTINATION share/${PROJECT_NAME}/
  )

ament_package()
