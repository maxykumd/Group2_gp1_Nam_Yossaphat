# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: main_lidar_node.py - Scenario 3 Lidar Node

import rclpy
from group2_gp1.lidar_node import LidarNode

def main() -> None:
    """
    Main runner/entry point for the LidarNode.
    """
    rclpy.init()

    lid_node = LidarNode()   # Initializes the CameraNode, which sets up the publisher and timer to start publishing frames at 5 Hz

    try:
        while rclpy.ok():
            rclpy.spin(lid_node) 
    except KeyboardInterrupt:
        lid_node.get_logger().info('Lidar node interrupted.')
    finally:
        lid_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
