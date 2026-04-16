# Name: Yossaphat Kulvatunyou
# UID: 112362550
# Module: run_logger_node.py

import rclpy
from group2_gp1.logger_node import LoggerNode


def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode("logger_node")
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Closing Logger_node")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()