# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: fusion_node.py - Scenario 3 Fusion Node

import json
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
        """
        Initialize the fusion node, including QoS profiles, callback groups, subscriptions, and publisher.
        """
        super().__init__('fusion_node')   # Node name is fusion_node, as specified in the launch file

        # QoS Profiles
        sensor_qos = QoSProfile(   # Follows Scenario 3 sensor QoS (System Architecture - Topics)
            depth=1,   # Depth of 1 since we only care about the latest frame, older frames can be dropped (explained in README.md)
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )

        fused_qos = QoSProfile(   # Follows Scenario 3 fused output QoS (System Architecture - Topics)
            depth=10,   # Depth of 10 to allow some buffering of fused messages, since downstream nodes may want to receive recent history (explained in README.md)
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE
        )

        config_qos = QoSProfile(   # QoS for config topic, can be different since it's a different use case (config updates rather than sensor data)
            depth=1,   # Only care about the latest config, older configs can be dropped (explained in README.md)
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )

        # Callback groups for shared state protection and independent timer execution

        # Shared state protection
        self._sensor_group = MutuallyExclusiveCallbackGroup()   # MutuallyExclusiveCallbackGroup is used because both callbacks modify shared state (_latest_frame and _latest_distance). This prevents race conditions when using a MultiThreadedExecutor (explained in README.md)

        # Timer runs independently
        self._timer_group = ReentrantCallbackGroup()   # ReentrantCallbackGroup allows the timer callback to run independently of sensor callbacks, ensuring fusion output is published at a fixed rate even if sensor callbacks are delayed (explained in README.md)

        # Internal State
        self._latest_frame = None   # 
        self._latest_distance = None

        self._fusion_rate = 5.0  # Default fusion rate is 5 Hz, can be updated via config topic
        self._alert_threshold = 2.0   # Default alert threshold is 2 meters, can be updated via config topic

        # Subscribers
        self._camera_sub = self.create_subscription(   # Subscribes to camera topic, QoS as defined above, callback is camera_callback, uses sensor_group callback group to protect shared state
            String,
            '/sensors/camera',
            self.camera_callback,
            sensor_qos,
            callback_group=self._sensor_group
        )

        self._lidar_sub = self.create_subscription(   # Subscribes to LiDAR topic, QoS as defined above, callback is lidar_callback, uses sensor_group callback group to protect shared state
            Float64,
            '/sensors/lidar',
            self.lidar_callback,
            sensor_qos,
            callback_group=self._sensor_group
        )

        self._config_sub = self.create_subscription(   # Subscribes to config topic, QoS as defined above, callback is config_callback, does not need to use sensor_group since it doesn't modify shared sensor state
            String,
            '/system/config',
            self.config_callback,
            config_qos
        )

        # Publisher
        self._publisher = self.create_publisher(   # Publisher for fused output, topic is /perception/fused, QoS as defined above
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

    # Callbacks
    def camera_callback(self, msg: String) -> None:
        """
        Callback for camera topic subscription.

        Args:
            msg (String): Incoming camera frame message.
        """
        self._latest_frame = msg.data

    def lidar_callback(self, msg: Float64) -> None:
        """
        Callback for LiDAR topic subscription.

        Args:
            msg (Float64): Incoming LiDAR distance message.
        """

        self._latest_distance = msg.data

    def config_callback(self, msg: String) -> None:
        """
        Callback for config topic subscription.

        Args:
            msg (String): Incoming config message.
        """
        try:
            config = json.loads(msg.data)
            self._fusion_rate = config.get('fusion_rate', 5.0)   # Update fusion rate if provided in config, default to 5.0 Hz if not specified
            self._alert_threshold = config.get('alert_threshold', 2.0)   # Update alert threshold if provided in config, default to 2.0 meters if not specified

            self.get_logger().info(f'Received config: {config}')
        except Exception as e:
            self.get_logger().error(f'Failed to parse config: {e}')

    def publish_fused(self) -> None:
        """Publish fused output (the camera and LiDAR data) at fixed rate."""
        if self._latest_frame is None or self._latest_distance is None:
            return

        msg = String()
        msg.data = f'Fused -- camera: {self._latest_frame}, lidar: {self._latest_distance:.2f} m'

        self._publisher.publish(msg)

        self.get_logger().info(msg.data)