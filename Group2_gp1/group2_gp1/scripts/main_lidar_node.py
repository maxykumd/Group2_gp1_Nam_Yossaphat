# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: main_lidar_node.py - Scenario 3 Lidar Node

import rclpy
from group2_gp1.lidar_node import LidarNode

def main(args=None):
    rclpy.init(args=args)
    node = LidarNode("lidar_node")
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Closing lidar_node")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
