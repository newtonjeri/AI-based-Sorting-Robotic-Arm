#include <chrono>
#include <functional>
#include <memory>
#include <vector>
#include <string>
#include <iostream>


#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "robotic_arm_msgs/msg/yolov8_inference.hpp"
using std::placeholders::_1;

using namespace std::chrono_literals;
const double PI = 3.141592653589793238463;

class DynamicFrameBroadcaster : public rclcpp::Node
{
public:

DynamicFrameBroadcaster()
: Node("dynamic_frame_tf2_broadcaster")
{
    tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
    subscription_ = this->create_subscription<robotic_arm_msgs::msg::Yolov8Inference>("/Yolov8_Inference", 10, std::bind(&DynamicFrameBroadcaster::transform_callback, this, _1));


}

private:
void transform_callback(const robotic_arm_msgs::msg::Yolov8Inference & msg) const
{
    //rclcpp::Time now = this->get_clock()->now();
    std::vector<std::string> message;
    std::vector<std::string> names;
    std::vector<geometry_msgs::msg::TransformStamped> t;
    message = msg.detected_obj_positions;
    names = msg.class_names;

    //send logger information only
    RCLCPP_INFO(this->get_logger(), "Received yolov8_inference message");
    //stream the message to the screen using the logger
    int j = 0; 
    int i = 0;
    int num = 0;
    int num_ = 0;
    for(j = 0; j < names.size(); j++)
    {
      std::ostringstream oss;
      oss << names[j] << j;
      RCLCPP_INFO(this->get_logger(), "%s", oss.str().c_str());

      
      //create rclcpp time to record time now
      rclcpp::Time now = this->now();
      //double x = now.seconds() * PI;

       geometry_msgs::msg::TransformStamped newint;
       t.push_back(newint);
       t[j].header.stamp = now;
       t[j].header.frame_id = "aruco_link";
       t[j].child_frame_id = oss.str();
    
    for(i = 0; i < (3); i++)
    {
        std::string message_position = message[num];
        //format to stream usign RCLCPP logger
        //RCLCPP_INFO(this->get_logger(), message_position.c_str());
        if(num_ == 0)
        { 
          double number = std::stod(message_position)/1000;
          //log number data to screen
          RCLCPP_INFO(this->get_logger(), "%f", number);
          t[j].transform.translation.y = number;
        }
        else if(num_ == 1)
        {
          double number = std::stod(message_position)/1000;
          //log number data to screen
          RCLCPP_INFO(this->get_logger(), "%f", number);
          t[j].transform.translation.x = number;
        }
        else if(num_ == 2)
        {
          double number = std::stod(message_position)/1000;
          //log number data to screen
          RCLCPP_INFO(this->get_logger(), "%f", number);
          t[j].transform.translation.z = number;
        }

        num++;
        num_++;
    }
        num_ = 0;
      tf_broadcaster_->sendTransform(t[j]);
    }


}

  rclcpp::TimerBase::SharedPtr timer_;
  std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::Subscription<robotic_arm_msgs::msg::Yolov8Inference>::SharedPtr subscription_;
  
  

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<DynamicFrameBroadcaster>());
  rclcpp::shutdown();
  return 0;
}