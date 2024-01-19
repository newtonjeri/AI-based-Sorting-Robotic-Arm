#include "robotic_arm_controllers/robotic_arm_hw_interface.hpp"
#include <hardware_interface/types/hardware_interface_type_values.hpp>
#include <pluginlib/class_list_macros.hpp>


namespace robotic_arm_controllers
{
RoboticArmHWInterface::RoboticArmHWInterface()
{
}


RoboticArmHWInterface::~RoboticArmHWInterface()
{
  if (arduino_port.IsOpen())
  {
    try
    {
      arduino_port.Close();
    }
    catch (...)
    {
      RCLCPP_FATAL_STREAM(rclcpp::get_logger("RoboticArmHWInterface"),
                          "Something went wrong while closing connection with port " << port_);
    }
  }
}


CallbackReturn RoboticArmHWInterface::on_init(const hardware_interface::HardwareInfo &hardware_info)
{
  CallbackReturn result = hardware_interface::SystemInterface::on_init(hardware_info);
  if (result != CallbackReturn::SUCCESS)
  {
    return result;
  }

  try
  {
    port_ = info_.hardware_parameters.at("port_");
  }
  catch (const std::out_of_range &e)
  {
    RCLCPP_FATAL(rclcpp::get_logger("RoboticArmHWInterface"), "No Serial Port provided! Aborting");
    return CallbackReturn::FAILURE;
  }

  position_commands.reserve(info_.joints.size());
  position_states.reserve(info_.joints.size());
  prev_position_commands.reserve(info_.joints.size());


  return CallbackReturn::SUCCESS;
}


std::vector<hardware_interface::StateInterface> RoboticArmHWInterface::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;

  // Provide only a position Interafce
  for (size_t i = 0; i < info_.joints.size(); i++)
  {
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &position_states[i]));
  }

  return state_interfaces;
}


std::vector<hardware_interface::CommandInterface> RoboticArmHWInterface::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  // Provide only a position Interafce
  for (size_t i = 0; i < info_.joints.size(); i++)
  {
    command_interfaces.emplace_back(hardware_interface::CommandInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &position_commands[i]));
  }

  return command_interfaces;
}


CallbackReturn RoboticArmHWInterface::on_activate(const rclcpp_lifecycle::State &previous_state)
{
  RCLCPP_INFO(rclcpp::get_logger("RoboticArmHWInterface"), "Starting robot hardware ...");

  // Reset commands and states
  position_commands = { 0.0, 0.0, 0.0, 0.0 , 0.0 };
  prev_position_commands = { 0.0, 0.0, 0.0, 0.0 , 0.0 };
  position_states = { 0.0, 0.0, 0.0, 0.0 , 0.0 };

  try
  {
    arduino_port.Open(port_);
    arduino_port.SetBaudRate(LibSerial::BaudRate::BAUD_9600);
  }
  catch (...)
  {
    RCLCPP_FATAL_STREAM(rclcpp::get_logger("RoboticArmHWInterface"),
                        "Something went wrong while interacting with port " << port_);
    return CallbackReturn::FAILURE;
  }

  RCLCPP_INFO(rclcpp::get_logger("RoboticArmHWInterface"),
              "Hardware started, ready to take commands");
  return CallbackReturn::SUCCESS;
}


CallbackReturn RoboticArmHWInterface::on_deactivate(const rclcpp_lifecycle::State &previous_state)
{
  RCLCPP_INFO(rclcpp::get_logger("RoboticArmHWInterface"), "Stopping robot hardware ...");

  if (arduino_port.IsOpen())
  {
    try
    {
      arduino_port.Close();
    }
    catch (...)
    {
      RCLCPP_FATAL_STREAM(rclcpp::get_logger("RoboticArmHWInterface"),
                          "Something went wrong while closing connection with port " << port_);
    }
  }

  RCLCPP_INFO(rclcpp::get_logger("RoboticArmHWInterface"), "Hardware stopped");
  return CallbackReturn::SUCCESS;
}

// Read the current states of the motors, servo angles, and send them to ros2
// Due to the limitation of our H/W openloop control is used, we assume the servo reach the desired positions
hardware_interface::return_type RoboticArmHWInterface::read(const rclcpp::Time &time,
                                                          const rclcpp::Duration &period)
{
  // Open Loop Control - assuming the robot is always where we command to be
  position_states = position_commands;
  return hardware_interface::return_type::OK;
}

// Send the desired joint position, servoangles
hardware_interface::return_type RoboticArmHWInterface::write(const rclcpp::Time &time,
                                                           const rclcpp::Duration &period)
{
  if (position_commands == prev_position_commands)
  {
    // Nothing changed, do not send any command
    return hardware_interface::return_type::OK;
  }



  std::string msg;
  int base_waist_joint = static_cast<int>((90 + (position_commands.at(0) * 180) / M_PI));
  msg.append("a");    //   base_waist_joint angle
  msg.append(std::to_string(base_waist_joint));
  msg.append(",");
  int waist_link1_joint = static_cast<int>((90 - (position_commands.at(1) * 180) / M_PI));
  msg.append("b");   //   waist_link1_joint angle
  msg.append(std::to_string(waist_link1_joint));
  msg.append(",");
  int link1_link2_joint = static_cast<int>((90 + (position_commands.at(2) * 180) / M_PI));
  msg.append("c");  //   link1_link2_joint angle
  msg.append(std::to_string(link1_link2_joint));
  msg.append(",");

  int link2_gripper_base_joint = static_cast<int>((90 - (position_commands.at(3) * 180) / M_PI));
  msg.append("d");  // link2_gripper_base_joint angle
  msg.append(std::to_string(link1_link2_joint));
  msg.append(",");

  int gripper = static_cast<int>(((position_commands.at(4)) * 180) / (M_PI / 2));
  msg.append("e");      //   gripper value
  msg.append(std::to_string(gripper));
  msg.append(",");
  msg.append("\n");      //   end of message

  try
  {
    if(i = 0)
    {
    RCLCPP_INFO_STREAM(rclcpp::get_logger("RoboticArmHWInterface"), "Sending new command " << msg);
    arduino_port.Write(msg);
    i = 1;
    }
  
  }
  catch (...)
  {
    RCLCPP_ERROR_STREAM(rclcpp::get_logger("RoboticArmHWInterface"),
                        "Something went wrong while sending the message "
                            << msg << " to the port " << port_);
    return hardware_interface::return_type::ERROR;
  }

  prev_position_commands = position_commands;

  return hardware_interface::return_type::OK;
}
}  // namespace robotic_arm_hwinterface

PLUGINLIB_EXPORT_CLASS(robotic_arm_controllers::RoboticArmHWInterface, hardware_interface::SystemInterface)