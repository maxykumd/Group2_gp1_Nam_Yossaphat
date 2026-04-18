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
        super().__init__('camera_node')   # Node name is camera_node, as specified in the launch file

        cam_qos = QoSProfile(   # Follows Scenario 3 camera sensor QoS (System Architecture - Topics)
            depth=1,   # Depth of 1 since we only care about the latest frame, older frames can be dropped (explained in README.md)
            reliability=ReliabilityPolicy.BEST_EFFORT,   # The intentional mismatch is explained in the README.md (Please refer to that)
            durability=DurabilityPolicy.VOLATILE
        )

        self._publisher = self.create_publisher(   # Publisher for camera frames, topic is /sensors/camera, QoS as defined above
            String,
            '/sensors/camera',
            cam_qos
        )

        self._frame_counter = 1 # Starting at frame_0001

        self._timer = self.create_timer(   # Publish at 10 Hz (as we discussed in lecture 0.1 seconds is 10 Hz)
            0.1,
            self._publish_frame
        )

    def _publish_frame(self) -> None:   # Helper function to publish the next camera frame ID, called by the timer every 0.1 seconds
        """
        Publish the next camera frame ID.
        """
        msg = String()
        msg.data = f'frame_{self._frame_counter:04d}'   # Formats the frame counter as zero-padded 4-digit number (example being frame_0001)

        self._publisher.publish(msg)

        self.get_logger().info(f'Publishing {msg.data}')

        self._frame_counter += 1

