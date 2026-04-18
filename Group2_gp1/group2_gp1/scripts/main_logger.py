# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: main_logger.py - Scenario 3 Main file for LoggerNode

import rclpy
from group2_gp1.logger import LoggerNode


def main() -> None:
    """
    Main runner/entry point for the LoggerNode.
    """
    rclpy.init()

    log_node = LoggerNode() 

    try:
        while rclpy.ok():
            rclpy.spin(log_node)  # Spin to process incoming /perception/fused messages
    except KeyboardInterrupt:
        log_node.get_logger().info('Logger node interrupted.')
    finally:
        log_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
