#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import numpy as np
from math import radians
from v2_service_interface.srv import SetScanFrequency

class LaserPublisherNode(Node):
    
    VALID_SCAN_FREQUENCIES = [5, 10, 15]

    def __init__(self):
        super().__init__('laser_data_publisher')
        self.scan= []
        self.laser_data_publisher=self.create_publisher(LaserScan,"scan",10)
        self.laser_data_timer=self.create_timer(0.1,self.publish_laser_data)
        self.get_logger().info("Node laser_data_publisher started.")

    def publish_laser_data(self):
        msg= LaserScan()
        msg.ranges=self.scan
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'
        msg.angle_min = np.radians(-90)  # -90 Grad in Radianten
        msg.angle_max = np.radians(90)   # +90 Grad in Radianten
        msg.angle_increment = np.radians(1)  # 1 Grad in Radianten (approx. 0.01745)
        msg.time_increment = 0.0  # Optional: Zeit zwischen Messungen
        msg.scan_time = 1.0 / self.current_frequency# Beispiel: 10 Hz
        msg.range_min = 0.15    
        msg.range_max = 10.0

        # Start: Generierung der simulierten Abstandswerte
        num_samples = int((msg.angle_max - msg.angle_min) /msg.angle_increment) + 1
        mean = 5.0
        std_dev = 1.2
        values = np.random.normal(loc=mean, scale=std_dev,size=num_samples)
        values = np.clip(values, msg.range_min, msg.range_max)
        # Ende: Generierung der simulierten Abstandswerte
        msg.ranges=values
        self.laser_data_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LaserPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
   main()