# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: lidar_node.py - Scenario 3 Lidar Node

from std_msgs.msg import Float64
from rclpy.node import Node
import random
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

class LidarNode(Node):
    """
    ROS 2 node that simulates LiDAR sensor data.
    Publishes std_msgs/msg/Float64 messages to '/sensors/lidar' at 5 Hz.

    Attributes:
        _publisher (Publisher): Publishes distance data to /sensors/lidar.
        _timer (Timer): Controls publishing rate (5 Hz).
        _message (Float64): Message object storing LiDAR distance.
        _counter (int): Counter for number of published readings.
    """
    
    def __init__(self, node_name: str):
        super().__init__(node_name)
        
        lidar_qos = QoSProfile(   # Follows Scenario 3 camera Ssensor QoS (System Architecture - Topics), need to make sure Specific Requirements point 2 later is "RELIABLE" to demonstrate intentional mismatch
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )

        self._counter = 0
        self._message = Float64()
        self._publisher = self.create_publisher(Float64, "/sensors/lidar", lidar_qos) #msg_type: Any,topic: str, qos_profile: QoSProfile 
        self._timer = self.create_timer(0.2, self.publish_simulate_reading)

    def publish_simulate_reading(self) -> None:
        """
        Timer callback that generates a random LiDAR distance reading
        and publishes it to the '/sensors/lidar' topic.
        """
        self._message.data = random.uniform(0.5, 50.0)
        self._publisher.publish(self._message)
        self.get_logger().info(f"Lidar Distance: {self._message.data:.2f} m")
        self._counter += 1
