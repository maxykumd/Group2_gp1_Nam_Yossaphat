# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: main_safety_monitor_node.py - Scenario 3 Main file for SafetyMonitorNode

import rclpy
from group2_gp1.safety_monitor import SafetyMonitor


def main(args=None):
    """
    Entry point for the SafetyMonitor node
    """
    rclpy.init(args=args)
    
    safety = SafetyMonitor("safety_monitor")
    
    try:
        rclpy.spin(safety) # Spin to process /perception/fused callbacks and publish alerts
    except KeyboardInterrupt:
        safety.get_logger().info("Closing safety_monitor")
    finally:
        safety.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
