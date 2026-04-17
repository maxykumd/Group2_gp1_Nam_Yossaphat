# Name: Nam Facchetti & Yossaphat Kulvatunyou
# Module: main_fusion_node.py - Scenario 3 Main file for FusionNode

import rclpy
from rclpy.executors import MultiThreadedExecutor
from group2_gp1.fusion_node import FusionNode

def main(args=None):
    rclpy.init(args=args)

    node = FusionNode()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Fusion node interrupted.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()