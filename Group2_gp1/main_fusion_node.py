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
        while rclpy.ok():
            executor.spin_once(timeout_sec=0.1)   # Spins the executor to process callbacks and timers, with a timeout to allow for shutdown on interrupt
    except KeyboardInterrupt:
        fuse_node.get_logger().info('Fusion node interrupted.')
    finally:
        fuse_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()