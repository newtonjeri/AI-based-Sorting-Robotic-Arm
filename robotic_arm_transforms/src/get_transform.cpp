#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "geometry_msgs/msg/point.hpp"
#include "tf2/exceptions.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "robotic_arm_msgs/msg/yolov8_inference.hpp"
#include "robotic_arm_msgs/msg/world_object_inference.hpp"
using std::placeholders::_1;

using namespace std::chrono_literals;

class FrameListener : public rclcpp::Node
{
public:
  FrameListener()
  : Node("tf2_frame_listener"),
    turtle_spawning_service_ready_(false),
    turtle_spawned_(false)
  {
    // Declare and acquire `target_frame` parameter
    target_frame_ = this->declare_parameter<std::string>("target_frame", "turtle1");

    tf_buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
    // Create a client to spawn a turtle
    

    // Create turtle2 velocity publisher
    publisher_ = this->create_publisher<geometry_msgs::msg::Point>("topic", 1);
    publisher_tf = this->create_publisher<robotic_arm_msgs::msg::WorldObjectInference>("world_object_inference", 10);
    subscription_ = this->create_subscription<robotic_arm_msgs::msg::Yolov8Inference>("/Yolov8_Inference", 10, std::bind(&FrameListener::on_timer, this, _1));


  }

private:
  void on_timer(const robotic_arm_msgs::msg::Yolov8Inference & msg)
  {
    // Store frame names in variables that will be used to
    // compute transformations
    std::string fromFrameRel = "world";
    //std::string toFrameRe[] ;
     
     std::vector<std::string> tf_data_class_names;
     std::vector<std::string> tf_data_detected_object_positions;
    robotic_arm_msgs::msg::WorldObjectInference tf_data;
    
    std::vector<std::string> names;
    std::vector<geometry_msgs::msg::TransformStamped> t;
    names = msg.class_names;

    
    for(int i = 0; i < names.size(); i++)
    {
        geometry_msgs::msg::TransformStamped t;

      tf_data_class_names.push_back(names[i]);
       
      
      std::ostringstream oss;
      oss << names[i] << i;
      RCLCPP_INFO(this->get_logger(), "%s", oss.str().c_str());

        try {
          t = tf_buffer_->lookupTransform(oss.str(), fromFrameRel, tf2::TimePointZero);

            tf_data_detected_object_positions.push_back(std::to_string(t.transform.translation.x));
            tf_data_detected_object_positions.push_back(std::to_string(t.transform.translation.y));
            tf_data_detected_object_positions.push_back(std::to_string(t.transform.translation.z));

        } 
        catch (const tf2::TransformException & ex) 
        {
            RCLCPP_INFO(this->get_logger(), "Could not transform %s to %s: %s",oss.str().c_str(), fromFrameRel.c_str(), ex.what());
          return;
        }

    }
       tf_data.class_names = tf_data_class_names;
       tf_data.detected_obj_positions = tf_data_detected_object_positions;
    
        publisher_tf->publish(tf_data);
    
  }

  // Boolean values to store the information
  // if the service for spawning turtle is available
  bool turtle_spawning_service_ready_;
  // if the turtle was successfully spawned
  int i = 0;
  bool turtle_spawned_;
  rclcpp::Subscription<robotic_arm_msgs::msg::Yolov8Inference>::SharedPtr subscription_;
  rclcpp::TimerBase::SharedPtr timer_{nullptr};
  rclcpp::Publisher<geometry_msgs::msg::Point>::SharedPtr publisher_{nullptr};
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};
  std::unique_ptr<tf2_ros::Buffer> tf_buffer_;
  std::string target_frame_;
  rclcpp::Publisher<robotic_arm_msgs::msg::WorldObjectInference>::SharedPtr publisher_tf;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FrameListener>());
  rclcpp::shutdown();
  return 0;
}