#!usr/bin/env python3

# Ros2 node to send data to arduino

import rclpy
from rclpy.node import Node
import serial

data = "a180,b90,c90,d90,e0,\n"
data_1 = "a0,b90,c90,d90,e0,\n"
data_2 = "a180,b90,c90,d90,e0,\n"
data_3 = "a0,b90,c90,d90,e0,\n"
data_4 = "a90,b90,c90,d90,e0,\n"

class SerialNode(Node):

    def __init__(self):
        super().__init__('serial_node')
        # Create a serial object with the port name and baud rate
        self.serial = serial.Serial('/dev/ttyUSB0', 9600)
        # Create a timer that will send data every second
        self.timer = self.create_timer(10.0, self.timer_callback)

    def timer_callback(self):
        # Write a byte to the serial port
        self.serial.write(data.encode('utf-8'))
        self.serial.write(data_1.encode('utf-8'))
        self.serial.write(data_2.encode('utf-8'))
        self.serial.write(data_3.encode('utf-8'))
        self.serial.write(data_4.encode('utf-8'))
        # Print the data
        self.get_logger().info('Data  Sent')
        # self.timer.cancel()


def main(args=None):
    rclpy.init(args=args)
    serial_node = SerialNode()
    rclpy.spin(serial_node)
    serial_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
