# Course: ENPM605 
### Section: 0101
### Professor: Zeid Kootbally
### Assignment: GP 1 (Scenario 3)
### Date: 04/17/2026


## Group Members:
Member 1: Nam Facchetti

UID: 118215693

Member 2: Yossaphat Kulvatunyou

UID: 112362550

## Scenario Summary:
This project implements a multi-node ROS 2 perception pipeline that simulates a simplified autonomous vehicle sensor fusion system. The system integrates asynchronous data streams from a camera and a LiDAR sensor, combines them into a unified perception output, and monitors safety conditions based on the fused data.

The architecture consists of six nodes: a camera node publishing image frame identifiers at 10 Hz, a LiDAR node publishing distance measurements at 5 Hz, a fusion node that synchronizes and combines the latest sensor readings, a safety monitor that evaluates obstacle proximity, a configuration publisher that distributes system parameters using latched QoS, and an optional logger node for recording system output. Communication between nodes is implemented using ROS 2 publishers and subscribers with explicitly defined Quality of Service (QoS) profiles.

A key feature of the system is the use of heterogeneous QoS policies tailored to different data streams. Sensor topics use BEST_EFFORT reliability with a depth of 1 to prioritize low-latency delivery of the most recent data, while fused perception and alert topics use RELIABLE delivery to ensure critical information is not lost. The configuration topic uses TRANSIENT_LOCAL durability, allowing late-joining nodes to receive the most recent system configuration without requiring re-publication.

The fusion node demonstrates concurrent execution using a MultiThreadedExecutor and carefully selected callback groups. Sensor callbacks share a MutuallyExclusiveCallbackGroup to protect shared state (latest camera frame and LiDAR reading), while the publishing timer operates in a ReentrantCallbackGroup to maintain a consistent output rate independent of sensor callback timing.

The system also intentionally includes a QoS mismatch scenario, where a RELIABLE subscriber attempts to connect to a BEST_EFFORT publisher, resulting in no data delivery. This demonstrates the importance of QoS compatibility and provides an opportunity to diagnose communication issues using ROS 2 introspection tools.

Overall, this project illustrates how independent ROS 2 nodes can be composed into a coherent, real-time system that balances performance, reliability, and modularity while leveraging advanced middleware features such as QoS policies, executors, and launch configurations.

## Node Graph:

## Design Decisions:
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

### Prerequisites
Ensure that ROS 2 (Humble or later) is installed and sourced on your system.
- source /opt/ros/humble/setup.bash

### Workspace Setup
Navigate to your ROS 2 workspace and place the package in the src/ directory:
- cd ~/enpm605_ws/src

Your package structure should look like:
- group2_gp1/

### Build the Package
Return to the workspace root and build the package:
- cd ~/enpm605_ws
- colcon build --packages-select group2_gp1

### Source the Workspace
After building, source the workspace:
- source install/setup.bash

### Run the System (Default Configuration)
Launch the full sensor fusion system:
- ros2 launch group2_gp1 system.launch.py

### Run with Logger Enabled
Enable the optional logger node using the launch argument:
- ros2 launch group2_gp1 system.launch.py enable_logger:=true

### Override Alert Threshold
Change the obstacle detection threshold (in meters):
- ros2 launch group2_gp1 system.launch.py alert_threshold:=5.0

### Verify System Operation
List all active topics and their message types:
- ros2 topic list -t

Monitor fused perception output:
- ros2 topic echo /perception/fused

Monitor safety alerts:
- ros2 topic echo /perception/alerts

Check camera publishing rate (should be about 10 Hz):
- ros2 topic hz /sensors/camera

Inspect QoS settings and detect mismatches:
- ros2 topic info /sensors/camera -v

### Test TRANSIENT_LOCAL Behavior
Verify that late-joining subscribers receive the configuration message:
- ros2 topic echo /system/config --once
This should immediately return the last published configuration.

### Visualize Node Graph
Use the ROS 2 graph tool to inspect node and topic connections:
- rqt_graph