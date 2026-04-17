# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: main_logger.py - Scenario 3 Main file for LoggerNode

import rclpy
from group2_gp1.logger import LoggerNode


def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode("logger")
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Closing logger")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
