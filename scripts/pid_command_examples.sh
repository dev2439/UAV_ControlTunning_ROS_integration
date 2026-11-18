#!/usr/bin/env bash
# Example ROS 2 commands for runtime PID tuning.

ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'list'}"
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'get kpr'}"
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'kpr=0.72'}"
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'get kpy'}"
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'kpy=2.90'}"
