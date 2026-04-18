# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: safety_monitor.py

from std_msgs.msg import String
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
import json

class SafetyMonitor(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        # share btw fused sub and alert pub
        self._group = MutuallyExclusiveCallbackGroup()
        
        # alert threshold ros parameter
        self.declare_parameter('alert_threshold', 2.0)
        self._threshold = self.get_parameter('alert_threshold').get_parameter_value().double_value
        self.get_logger().info(f"Alert threshold set to {self._threshold} m")
        
        # Publisher for alert
        alert_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self._alert_publishers = self.create_publisher(
            String, '/perception/alerts', alert_qos)
        
        # Subscriber to fused
        fused_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self._fused_sub = self.create_subscription(
            String,'/perception/fused',self.fused_callback,fused_qos,callback_group=self._group,)
        
        # Subscriber to config
        config_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self._config_sub = self.create_subscription(
            String, '/system/config', self.config_callback, config_qos)

        # intentional mismatch subscriber 
        """
        The mismatch subscriber use realiability=RELIABLE to sub to /sensors/camera
        which is pub with reliability=BEST_EFFORT. These 2 policy cant work tgt in ros2
        RELIABLE require pub to gurantee delivery which BEST_EFFORT dont gurantee
        -> SO, the sub will receive no data

        The ros2 topic info /sensors/camera -v will show pub use BEST_EFFORT and sub requiest RELIABLE
        and ros2 will list this as incompatible
        """
        mismatch_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
        )
        self._mismatch_sub = self.create_subscription(
            String, '/sensors/camera', self.mismatch_callback, mismatch_qos)


    def fused_callback(self, msg) -> None:
        """
        Parse fuse msg and check lidar distance
        """
     
        data = msg.data
        try:
            infos = data.split(',')
            lidar_info = infos[1]
            distance = float(lidar_info.split(':')[1].strip().split(' ')[0]) # Get lidar dist from string
        except ValueError as e:
            self.get_logger().error(f"Fail to parse fuse msg {data}:{e}")
            return
        
        if distance < self._threshold:
            # Log warning
            self.get_logger().warn(f"Obstacle at {distance} m (threshold: {self._threshold} m)")

            # Publish alert
            alert_msg = String()
            alert_msg.data = f"Obstacle at {distance}m is too close"
            self._alert_publishers.publish(alert_msg)
        
        else: # normal situation
            self.get_logger().info(data)


    def mismatch_callback(self, msg: String) -> None:
        self.get_logger().warn("This should NEVER print cause of mismatch fail")

    def config_callback(self, msg: String) -> None:
        """
        Receive sys config and update alert threshold
        Expect to receive json string format msg {"fuse_rate": 5, "alert_threshold": 2}
        """
        try:
            config = json.loads(msg.data)
            self._threshold = float(config.get("alert_threshold", 2.0))
            self.get_logger().info(f"Config received and threshold update to {self._threshold}m")
        except ValueError as e:
            self.get_logger().error(f"Failed to parse config msg: {e}")