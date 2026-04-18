# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: main_camera_node.py - Scenario 3 Main file for CameraNode

import rclpy
from group2_gp1.camera_node import CameraNode

def main() -> None:
    """
    Main runner/entry point for the CameraNode.
    """
    rclpy.init()

    cam_node = CameraNode()   # Initializes the CameraNode, which sets up the publisher and timer to start publishing frames at 10 Hz

    try:
        while rclpy.ok():
            rclpy.spin(cam_node)   # Keeps the node alive and responsive to the timer callback that publishes camera frames every 0.1 seconds (10 Hz)
    except KeyboardInterrupt:
        cam_node.get_logger().info('Camera node interrupted.')
    finally:
        cam_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
