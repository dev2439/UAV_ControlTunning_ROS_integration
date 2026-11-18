from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='uart_pid_bridge',
            executable='uart_pid_to_ros',
            name='uart_pid_bridge_node',
            output='screen',
        )
    ])
