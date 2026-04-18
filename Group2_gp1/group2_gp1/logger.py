# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: logger.py - Scenario 3 Logger Node

from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String

class LoggerNode(Node):
    """
    Subscribes to the /perception/fused topic and logs each message
    with a timestamp. Only started when enable_logger:=true is passed
    to the launch file via IfCondition.

    Attributes:
        _subscription (Subscription): Subscribes to /perception/fused.
    """
    def __init__(self, node_name: str ) -> None:
        super().__init__(node_name)

        fuse_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self._subscription = self.create_subscription(
            String, '/perception/fused', self.log_callback, fuse_qos)


    def log_callback(self, msg: str) -> None:
        """Log each fused message with a timestamp.

        Args:
            msg (String): The fused message from /perception/fused,
                formatted as 'camera: <frame_id>, lidar: <distance> m'.
        """
        # Get current time
        current = self.get_clock().now().to_msg()
        self.get_logger().info(f"[{current.sec}.{current.nanosec}] {msg.data}")
