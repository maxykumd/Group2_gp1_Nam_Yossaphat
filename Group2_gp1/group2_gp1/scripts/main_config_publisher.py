# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: main_config_publisher.py - Scenario 3 Configuration Publisher Node

import rclpy
from group2_gp1.config_publisher import ConfigPublisher

def main(args=None):
    """
    Entry point for the ConfigPublisher node. Initializes the node and spins it to publish the configuration once at startup. The node will automatically shut down after publishing the config due to the one-shot timer in the ConfigPublisher class.
    """
    rclpy.init(args=args)

    config_pub_node = ConfigPublisher()   # Node name is config_publisher, as specified in the launch file

    try:
        while rclpy.ok():
            rclpy.spin_once(config_pub_node, timeout_sec=0.1)   # Spins the node to allow it to publish the configuration message. The one-shot timer in the ConfigPublisher class will trigger the publication of the config message immediately after startup, and then the node will shut down after publishing. The loop with spin_once allows for shutdown on interrupt while waiting for the timer callback to execute.
    except KeyboardInterrupt:
        config_pub_node.get_logger().info('Config publisher interrupted.')
    finally:
        config_pub_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()