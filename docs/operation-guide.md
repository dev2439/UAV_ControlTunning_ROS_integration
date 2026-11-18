# Operation Guide

## Objective

This package supports a field workflow where a Raspberry Pi running ROS 2 communicates with a Teensy-based flight controller through UART. The same link is used for:

- telemetry monitoring;
- runtime PID tuning;
- command/response validation;
- remote operation from SSH.

In the current setup, the system is operated from an iPad connected to the Raspberry Pi through a small Wi-Fi network created with a phone hotspot.

---

## Recommended terminal layout

Use **two SSH terminals**:

### Session 1

Keep the ROS 2 node running here.

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run uart_pid_bridge uart_pid_to_ros
```

Expected message:

```text
[INFO] [...] [uart_pid_bridge_node]: Abriendo UART: /dev/serial0 @ 57600
```

### Session 2

Use this terminal for observation and PID commands.

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

---

## Serial mode logic

### Telemetry mode

Telemetry is available when:

- the system is armed; or
- the system is disarmed and **SWB is up**.

Useful commands:

```bash
ros2 topic echo /drone_uart_line
ros2 topic echo /roll_rel
ros2 topic echo /pitch_rel
ros2 topic echo /rate_yaw_f
```

### PID configuration mode

PID configuration is enabled when:

- the system is disarmed; and
- **SWB is down**.

Recommended first command:

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'list'}"
```

Then read the answer:

```bash
ros2 topic echo /pid_rx std_msgs/msg/String
```

---

## Available runtime parameters

### Inner loop

- `kpr`, `tir`, `tdr`
- `kpp`, `tip`, `tdp`
- `kpy`, `tiy`, `tdy`

### Outer loop

- `kproll`
- `kppitch`

---

## Common commands

### Read all parameters

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'list'}"
```

### Read one parameter

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'get kpr'}"
```

### Change one parameter

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'kpr=0.72'}"
```

---

## Example tuning sequence

1. Keep the vehicle **disarmed**.
2. Move **SWB down**.
3. Send `get kpr`.
4. Send `kpr=0.72`.
5. Send `get kpr` again to confirm the new value.
6. Return **SWB up**.
7. Perform a short test flight.

---

## Troubleshooting

### The node starts but no telemetry appears

Check:

- Teensy power;
- UART wiring and common ground;
- correct serial port;
- that the system is armed or SWB is up.

### `list` does not respond

Check:

- system is disarmed;
- SWB is really down;
- node is still alive;
- command syntax is correct.

### `/pid_rx` remains empty

Check:

- the controller is in PID configuration mode;
- a command was actually sent on `/pid_cmd`;
- you are not looking at telemetry instead of configuration responses.

### The port stops working after using another serial tool

If `miniterm` or another terminal takes ownership of `/dev/serial0`, close it before relaunching the ROS 2 node.
