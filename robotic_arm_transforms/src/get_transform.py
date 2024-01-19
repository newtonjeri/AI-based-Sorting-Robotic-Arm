import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Point
from robotic_arm_msgs.msg import Yolov8Inference
from tf2_ros import Buffer, TransformListener
from tf2_ros.exceptions import TransformException
from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf2_msgs.msg import TFMessage
import time

class FrameListener(Node):
    def __init__(self):
        super().__init__('tf2_frame_listener')
        self.get_logger().info('Python version of tf2_frame_listener is running')

        # Declare and acquire `target_frame` parameter
        self.target_frame = self.declare_parameter('target_frame', 'turtle1')

        self.tf_buffer = Buffer(self.get_clock())
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Create turtle2 velocity publisher
        self.publisher = self.create_publisher(Point, 'topic', QoSProfile(depth=1))
        self.subscription = self.create_subscription(
            Yolov8Inference, '/Yolov8_Inference', self.on_timer, QoSProfile(depth=10)
        )

    def on_timer(self, msg):
        # Store frame names in variables that will be used to
        # compute transformations
        from_frame_rel = 'world'

        for i in range(len(msg.class_names)):
            names = msg.class_names[i]
            oss = f'{names}{i}'
            self.get_logger().info(oss)

            try:
                t = self.tf_buffer.lookup_transform(oss, from_frame_rel, self.get_clock().now())

                msg_ = Point()
                msg_.x = t.transform.translation.x
                msg_.y = t.transform.translation.y
                msg_.z = t.transform.translation.z

                self.get_logger().info("linear x: %f  msg x: %f", t.transform.translation.x, msg_.x)
                self.get_logger().info("linear y: %f  msg y: %f", t.transform.translation.y, msg_.y)
                self.get_logger().info("linear z: %f  msg z: %f", t.transform.translation.z, msg_.z)

            except TransformException as ex:
                self.get_logger().info(
                    "Could not transform %s to %s: %s", oss, from_frame_rel, ex)
                return

            self.publisher.publish(msg_)

def main(args=None):
    rclpy.init(args=args)
    node = FrameListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
