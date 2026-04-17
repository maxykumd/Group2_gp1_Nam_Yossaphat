# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: main_safety_monitor_node.py - Scenario 3 Main file for SafetyMonitorNode

import rclpy
from group2_gp1.safety_monitor import SafetyMonitor


def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitor("safety_monitor")
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Closing safety_monitor")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
