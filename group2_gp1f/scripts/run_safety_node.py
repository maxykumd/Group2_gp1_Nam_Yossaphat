# Name: Yossaphat Kulvatunyou & Nam Facchett
# Module: run_safety_node.py

import rclpy
from group2_gp1f.safety_node import SafetyMonitor


def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitor("safety_node")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Closing safety_node")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
