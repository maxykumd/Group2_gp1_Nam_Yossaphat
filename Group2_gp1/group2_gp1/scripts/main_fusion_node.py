# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: main_fusion_node.py - Scenario 3 Main file for FusionNode

import rclpy
from rclpy.executors import MultiThreadedExecutor
from group2_gp1.fusion_node import FusionNode

def main(args: list[str] | None = None) -> None:
    """
    Entry point for the FusionNode using a MultiThreadedExecutor.
    """
    rclpy.init(args=args)

    fuse_node = FusionNode()   # Initializes the FusionNode, which sets up the subscribers, publisher, and timer for fusion output

    executor = MultiThreadedExecutor()   # Using MultiThreadedExecutor to allow concurrent execution of callbacks (camera, LiDAR, config) and timer for fusion output, while the callback groups ensure thread safety for shared state (explained in README.md)
    executor.add_node(fuse_node)   # Adds the fusion node to the executor so that its callbacks and timer can be executed concurrently

    try:
        executor.spin()   # Spins the executor to start processing callbacks and timers for the fusion node. The fusion output will be published at a fixed rate (default 5 Hz) regardless of the timing of incoming camera and LiDAR messages, due to the use of a ReentrantCallbackGroup for the timer (explained in README.md)
    except KeyboardInterrupt:
        fuse_node.get_logger().info('Fusion node interrupted.')
    finally:
        fuse_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()