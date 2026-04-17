# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: main_config_publisher.py - Scenario 3 Configuration Publisher Node

import rclpy
from group2_gp1f.config_node import ConfigPublisher

def main(args=None):
    rclpy.init(args=args)

    node = ConfigPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Config publisher interrupted.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()