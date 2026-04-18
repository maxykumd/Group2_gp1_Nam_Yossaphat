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
        rclpy.spin(config_pub_node)   # Spin the node to allow it to publish the config message once, then it will automatically stop due to the one-shot timer in the ConfigPublisher class
    except KeyboardInterrupt:
        config_pub_node.get_logger().info('Config publisher interrupted.')
    finally:
        config_pub_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()