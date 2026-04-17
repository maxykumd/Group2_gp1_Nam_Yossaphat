# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: camera_node.py - Scenario 3 Camera Node

from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String

class CameraNode(Node):
    """
    Publishes simulated camera frame IDs at 10 Hz.

    Attributes:
        _publisher (Publisher): Publishes frame IDs to /sensors/camera.
        _timer (Timer): Controls publishing rate/frequency.
        _frame_counter (int): Frame counter.
    """

    def __init__(self) -> None:
        """
        Initialize the camera publisher node.
        """
        super().__init__('camera_node')

        cam_qos = QoSProfile(   # Follows Scenario 3 camera sensor QoS (System Architecture - Topics), need to make sure Specific Requirements point 2 later is "RELIABLE" to demonstrate intentional mismatch
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )

        self._publisher = self.create_publisher(
            String,
            '/sensors/camera',
            cam_qos
        )

        self._frame_counter = 1 # Starting at frame_0001

        self._timer = self.create_timer(   # Publish at 10 Hz (as we discussed in lecture 0.1 seconds is 10 Hz)
            0.1,
            self._publish_frame
        )

    def _publish_frame(self) -> None:
        """
        Publish the next camera frame ID.
        """
        msg = String()
        msg.data = f'frame_{self._frame_counter:04d}'   # Formats the frame counter as zero-padded 4-digit number (example being frame_0001)

        self._publisher.publish(msg)

        self.get_logger().info(f'Publishing {msg.data}')

        self._frame_counter += 1

