# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: logger.py - Scenario 3 Logger Node

from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String

class LoggerNode(Node):
    def __init__(self, node_name: String ):
        super().__init__(node_name)

        self._enable = False

        fuse_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self._subscription = self.create_subscription(
            String, '/perception/fused', self.log_callback, fuse_qos)


    def log_callback(self, msg: String) -> None:
        if not self._enable:
            return
        
        # Get current time
        current = self.get_clock().now().to_msg()
        self.get_logger().info(f"[{current.sec}.{current.nanosec}] {msg.data}")
