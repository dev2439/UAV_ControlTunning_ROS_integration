# Quick Commands

## Session 1 — Start the ROS 2 bridge

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run uart_pid_bridge uart_pid_to_ros
```

## Session 2 — Basic checks

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 node list
ros2 topic list -t
ros2 topic echo /drone_uart_line
```

## PID configuration mode commands

Use these only when the system is **disarmed** and **SWB is down**.

### List all parameters

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'list'}"
```

### Read one parameter

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'get kpr'}"
```

### Write one parameter

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'kpr=0.72'}"
```

### Watch firmware responses

```bash
ros2 topic echo /pid_rx std_msgs/msg/String
```

## Telemetry watch examples

```bash
ros2 topic echo /roll_rel
ros2 topic echo /pitch_rel
ros2 topic echo /rate_roll_f
ros2 topic echo /rate_pitch_f
ros2 topic echo /rate_yaw_f
```
