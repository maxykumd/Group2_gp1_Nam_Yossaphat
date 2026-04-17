# Name: Yossaphat Kulvatunyou & Nam Facchetti
# Module: system.launch.py - Scenario 3 Sensor Fusion Pipeline Launch File

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch file for the Sensor Fusion Pipeline (Scenario 3).

    Starts the following nodes:
        - config_node: publishes system config once at startup
        - camera_node: publishes simulated camera frames at 10 Hz
        - lidar_node: publishes simulated LiDAR distance at 5 Hz
        - fusion_node: fuses camera and LiDAR data, publishes at 5 Hz

        - safety_monitor: monitors fused output and publishes alerts
        - logger (optional): logs fused output, started only if enable_logger:=true

    Launch arguments:
        enable_logger (bool, default: false): conditionally starts the logger node
        alert_threshold (float, default: 2.0): LiDAR distance threshold for alerts

    Usage:
        ros2 launch group2_gp1f system.launch.py
        ros2 launch group2_gp1f system.launch.py enable_logger:=true
        ros2 launch group2_gp1f system.launch.py alert_threshold:=5.0
    """


    # launch with arguments
    enable_logger_arg = DeclareLaunchArgument(
        'enable_logger',
        default_value='false',
        description='Set to true to start the logger node'
    )

    alert_threshold_arg = DeclareLaunchArgument(
        'alert_threshold',
        default_value='2.0',
        description='lidar distance threshold (meters) for safety alerts'
    )


    # Node grouping 
    sensor_group = GroupAction([
        Node(
            package='group2_gp1f',
            executable='run_camera_node',
            name='camera_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='group2_gp1f',
            executable='run_lidar_node',
            name='lidar_node',
            output='screen',
            emulate_tty=True,
        ),
    ])


    config_node = Node(
        package='group2_gp1f',
        executable='run_config_node',
        name='config_publisher',
        output='screen',
        emulate_tty=True,
    )


    fusion_node = Node(
        package='group2_gp1f',
        executable='run_fusion_node',
        name='fusion_node',
        output='screen',
        emulate_tty=True,
    )


    safety_monitor_node = Node(
        package='group2_gp1f',
        executable='run_safety_node',
        name='safety_monitor',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'alert_threshold': LaunchConfiguration('alert_threshold')
        }],
    )

    # condition launching from argument
    logger_node = Node(
        package='group2_gp1f',
        executable='run_logger_node',
        name='loggerss',
        output='screen',
        emulate_tty=True,
        condition=IfCondition(LaunchConfiguration('enable_logger')),
    )

    return LaunchDescription([
        enable_logger_arg,
        alert_threshold_arg,
        #config_node,
        sensor_group,
        fusion_node,
        safety_monitor_node,
        logger_node,
    ])