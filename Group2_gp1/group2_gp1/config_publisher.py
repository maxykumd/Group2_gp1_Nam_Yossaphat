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
        super().__init__('config_publisher')

        # QoS: RELIABLE + TRANSIENT_LOCAL (latched behavior)
        config_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )

        self._publisher = self.create_publisher(
            String,
            '/system/config',
            config_qos
        )

        # One-shot timer to publish once after startup
        self._timer = self.create_timer(
            0.5,  # small delay ensures publisher is ready
            self._publish_config
        )

    def _publish_config(self) -> None:
        """
        Publish configuration once, then stop timer.
        """
        config = {
            "fusion_rate": 5,
            "alert_threshold": 2.0
        }

        msg = String()
        msg.data = json.dumps(config)

        self._publisher.publish(msg)

        self.get_logger().info(f'Published system config: {msg.data}')

        # Stop timer so it only runs once
        self._timer.cancel()