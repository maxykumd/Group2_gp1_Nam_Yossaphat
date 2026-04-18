# Course: ENPM605 
## Section: 0101
## Professor: Zeid Kootbally
### Assignment: GP 1 (Scenario 3)
### Date: 04/17/2026


## Group Members:

Member 1: Nam Facchetti
UID: 118215693

Member 2: Yossaphat Kulvatunyou
UID: 112362550

## Scenario Summary:

## Node Graph:

## Design Decisions:

(including depth-1 sensor choice)

camera_node: The camera_node publishes simulated image frame IDs at 10 Hz on the /sensors/camera topic using the std_msgs/msg/String message type. A BEST_EFFORT, VOLATILE QoS profile with depth 1 was selected to reflect real-time perception system behavior, where only the most recent sensor data is relevant and older messages can be safely dropped. This minimizes latency and memory usage while ensuring high-frequency data flow. The node uses a timer-based callback to simulate a continuous camera stream, incrementing a frame counter and formatting it as a zero-padded string (for example, frame_0001).

The camera_node uses BEST_EFFORT reliability, which is intentionally incompatible with a RELIABLE subscriber used elsewhere in the system to demonstrate QoS mismatch behavior. This mismatch results in no data delivery, which can be verified using: ros2 topic info /sensors/camera -v

lidar_node: 

fusion_node: MutuallyExclusiveCallbackGroup is used for camera and LiDAR callbacks to prevent race conditions when updating shared state (_latest_frame, _latest_distance) under a MultiThreadedExecutor. ReentrantCallbackGroup is used for the fusion timer so it can execute independently of sensor callbacks and maintain a consistent publishing rate. Depth = 1 for sensors ensures only the most recent data is used, mimicking real-time perception systems and avoiding stale sensor data. TRANSIENT_LOCAL config topic allows late-joining nodes to receive configuration immediately.

safety_monitor: 

logger: 

config_publisher: TRANSIENT_LOCAL ensures that late-joining subscribers (like fusion_node and safety_monitor) will still receive the last published configuration message. This mimics latched behavior. Additionally, A short delay ensures that subscribers have time to connect before publishing. Without this, some nodes might miss the message even with TRANSIENT_LOCAL.

The configuration is published using a one-shot timer with a short delay (0.5 seconds). This ensures that the publisher is fully initialized Subscribers have time to connect and after publishing, the timer is canceled to prevent repeated messages.

A depth of 1 is used because only the most recent configuration is relevant. Older configurations are not needed and should not be buffered.

## Build/Run Instructions: