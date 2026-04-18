# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: config_publisher.py - Scenario 3 Configuration Publisher Node

import json
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String

class ConfigPublisher(Node):
    """
    Publishes system configuration once at startup using TRANSIENT_LOCAL durability.

    Attributes:
        _publisher (Publisher): Publishes config message to /system/config.
        _timer (Timer): One-shot timer to publish config.
    """

    def __init__(self) -> None:
        """
        Initialize the config publisher node, including QoS profile and one-shot timer.
        """
        super().__init__('config_publisher')   # Node name is config_publisher, as specified in the launch file

        config_qos = QoSProfile(   # Follows Scenario 3 config publisher QoS (System Architecture - Topics)
            depth=1,   # Depth of 1 since we only need to publish the config once, and late-joining nodes should get the latest config (explained in README.md)
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL   # TRANSIENT_LOCAL durability ensures late-joining nodes receive the last published config message, which is important for system configuration (explained in README.md)
        )

        self._publisher = self.create_publisher(   # Publisher for system config, topic is /system/config, QoS as defined above
            String,
            '/system/config',
            config_qos
        )

        # One-shot timer to publish once after startup
        self._timer = self.create_timer(   # Small delay ensures publisher is ready before publishing config
            0.5,
            self._publish_config
        )

    def _publish_config(self) -> None:
        """
        Publish configuration once, then stop timer.
        """
        config = {
            "fusion_rate": 5,   # Fusion node publishes at 5 Hz, so config publisher includes this info in the config message for late-joining nodes (explained in README.md)
            "alert_threshold": 2.0   # Default LiDAR distance threshold for safety alerts, included in config message for late-joining nodes (explained in README.md)
        }

        msg = String()
        msg.data = json.dumps(config)

        self._publisher.publish(msg)

        self.get_logger().info(f'Published system config: {msg.data}')

        self._timer.cancel()   # Stop the timer after publishing config once