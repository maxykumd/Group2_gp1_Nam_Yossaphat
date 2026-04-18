# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: main_safety_monitor_node.py - Scenario 3 Main file for SafetyMonitorNode

import rclpy
from group2_gp1.safety_monitor import SafetyMonitor


def main() -> None:
    """
    Main runner/entry point for the SafetyMonitor node.
    """
    rclpy.init()

    safety = SafetyMonitor("safety_monitor") 

    try:
        while rclpy.ok():
            rclpy.spin(safety)   # Spin to process /perception/fused callbacks and publish alert
    except KeyboardInterrupt:
        safety.get_logger().info('Safety node interrupted.')
    finally:
        safety.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
