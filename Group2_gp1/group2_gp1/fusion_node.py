# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: fusion_node.py - Scenario 3 Fusion Node

from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from std_msgs.msg import String, Float64


class FusionNode(Node):
    """
    Fuses camera and LiDAR data and publishes a combined perception message.

    Attributes:
        _sensor_group (MutuallyExclusiveCallbackGroup): Protects shared sensor state.
        _timer_group (ReentrantCallbackGroup): Allows timer to run independently.

        _latest_frame (str | None): Most recent camera frame.
        _latest_distance (float | None): Most recent LiDAR distance.

        _fusion_rate (float): Fusion publish rate (Hz).
        _alert_threshold (float): Threshold for obstacle detection.

        _camera_sub (Subscription): Camera subscriber.
        _lidar_sub (Subscription): LiDAR subscriber.
        _config_sub (Subscription): Config subscriber.

        _publisher (Publisher): Publishes fused output.
        _timer (Timer): Controls fusion output rate.
    """

    def __init__(self) -> None:
        super().__init__('fusion_node')

        # QoS Profiles
        sensor_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )

        fused_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE
        )

        config_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )

        # Callback Groups

        # Shared state protection
        self._sensor_group = MutuallyExclusiveCallbackGroup()

        # Timer runs independently
        self._timer_group = ReentrantCallbackGroup()

        # Internal State
        self._latest_frame = None
        self._latest_distance = None

        self._fusion_rate = 5.0  # default
        self._alert_threshold = 2.0

        # Subscribers
        self._camera_sub = self.create_subscription(
            String,
            '/sensors/camera',
            self.camera_callback,
            sensor_qos,
            callback_group=self._sensor_group
        )

        self._lidar_sub = self.create_subscription(
            Float64,
            '/sensors/lidar',
            self.lidar_callback,
            sensor_qos,
            callback_group=self._sensor_group
        )

        self._config_sub = self.create_subscription(
            String,
            '/system/config',
            self.config_callback,
            config_qos
        )

        # Publisher
        self._publisher = self.create_publisher(
            String,
            '/perception/fused',
            fused_qos
        )

        # Timer
        self._timer = self.create_timer(
            1.0 / self._fusion_rate,
            self.publish_fused,
            callback_group=self._timer_group
        )

    # Add back in when Yos finishes

    def camera_callback(self, msg: String) -> None:
        """Store latest camera frame."""
        self._latest_frame = msg.data

    def lidar_callback(self, msg: Float64) -> None:
        """Store latest LiDAR distance."""
        self._latest_distance = msg.data

    def config_callback(self, msg: String) -> None:
        """Parse config JSON string."""
        import json

        try:
            config = json.loads(msg.data)
            self._fusion_rate = config.get('fusion_rate', 5.0)
            self._alert_threshold = config.get('alert_threshold', 2.0)

            self.get_logger().info(f'Received config: {config}')
        except Exception as e:
            self.get_logger().error(f'Failed to parse config: {e}')

    def publish_fused(self) -> None:
        """Publish fused output at fixed rate."""
        if self._latest_frame is None or self._latest_distance is None:
            return

        msg = String()
        msg.data = f'Fused -- camera: {self._latest_frame}, lidar: {self._latest_distance:.2f} m'

        self._publisher.publish(msg)

        self.get_logger().info(msg.data)