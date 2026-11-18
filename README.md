# 🚁 UAV ROS 2 UART Bridge for Runtime PID Tuning

![ROS 2](https://img.shields.io/badge/ROS%202-Humble-22314E?logo=ros)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20%2B%20Teensy-6CC04A)
![Interface](https://img.shields.io/badge/Interface-UART-orange)
![Application](https://img.shields.io/badge/Application-UAV%20Control%20Tuning-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 📘 Overview

This repository provides a **ROS 2 middleware layer** for a UAV test platform where a **Raspberry Pi** communicates with a **Teensy-based flight controller** through **UART**.

Its main purpose is to support **runtime controller tuning during field tests**, allowing the operator to:

- monitor live telemetry from the flight controller;
- publish ROS 2 topics from UART data;
- inspect active PID parameters;
- modify controller gains without reflashing firmware between short flights.

In the current deployment, the ROS 2 node runs on the Raspberry Pi, while the system is operated remotely from an **iPad over SSH**. Both the **iPad** and the **Raspberry Pi** connect to the **phone hotspot**, which acts as the portable field Wi-Fi network.

## 🔗 Relation to the Main UAV Project

This repository is part of a broader UAV development stack and focuses on the **ROS 2 communication and field-tuning layer**.

It is linked to the main UAV project:

👉 **DIY_UAV (main repository)**  
🔗 https://github.com/dev2439/DIY_UAV

The `DIY_UAV` repository contains the main flight-controller firmware, embedded integration, and the overall vehicle development workflow. This ROS 2 repository complements it by enabling **runtime telemetry monitoring** and **PID tuning during field tests**.

## ✨ Features

- Bidirectional **UART ↔ ROS 2** communication
- Real-time publication of raw serial telemetry
- Parsed ROS 2 topics for key flight variables
- Runtime PID parameter inspection with `list` and `get`
- Runtime PID parameter updates through ASCII commands
- Echo topic for transmitted parameter commands
- Portable field workflow using Raspberry Pi + iPad + SSH
- Lightweight architecture for iterative controller tuning

## 📂 Contents

### 🧩 ROS 2 Package and Middleware Layer

- `/uart_pid_bridge/` → ROS 2 Python node for UART bridge and topic publication
- `/launch/` → launch file for the bridge node
- `/docs/` → operation notes, field workflow, and command references
- `/scripts/` → small command helpers for field use

### ⚙️ Package Configuration

- `package.xml`
- `setup.py`
- `setup.cfg`

## 🏗️ Architecture

<p align="center">
  <img src="https://github.com/user-attachments/assets/530acb0a-e876-40b0-82df-e4e41fafcd73" alt="ROS 2 UART PID bridge architecture" width="600">
</p>

### 🔄 Data Flow

1. The **Teensy** runs the onboard flight controller.
2. The serial channel carries either **telemetry frames** or **PID configuration responses**.
3. The **Raspberry Pi** runs the ROS 2 bridge node and republishes UART data into topics.
4. The operator connects remotely from an **iPad via SSH**, with both the iPad and the Raspberry Pi attached to the **phone hotspot**.
5. Commands such as `list`, `get kpr`, or `kpr=0.70` are sent through a second terminal session.


## 🔌 Raspberry Pi ↔ Teensy UART Wiring

The following schematic shows the basic UART wiring used between the **Raspberry Pi** and the **Teensy-based flight controller** for telemetry and runtime PID parameter tuning.

<p align="center">
  <img src="https://github.com/user-attachments/assets/14b1494d-2020-4169-a208-f78ead0cd2fc" alt="Raspberry Pi to Teensy UART wiring" width=600">
</p>

### 🧷 Wiring overview

- **Raspberry Pi TXD0 / GPIO14** → **Teensy RX1**
- **Raspberry Pi RXD0 / GPIO15** ← **Teensy TX1**
- **Raspberry Pi GND** ↔ **Teensy GND**

### ⚠️ Notes

- The UART link is **3.3 V logic level**.
- Only **TX, RX, and GND** are required for this communication link.
- Do **not** use this connection as a shared power line between boards.
- Make sure that both devices share a **common ground** for reliable serial communication.


## 🧰 Hardware and Field Setup

Typical field arrangement:

- **Flight controller:** Teensy-based UAV controller
- **Middleware computer:** Raspberry Pi running ROS 2
- **Physical link:** UART between Raspberry Pi and Teensy
- **Remote terminal:** iPad using SSH
- **Portable network:** phone hotspot, with both the iPad and the Raspberry Pi connected to it

This setup allows tuning and telemetry monitoring in the field without requiring a full laptop-based workflow.


## 🛠️ Full Experimental Setup

The following image shows the complete experimental setup used during field tests, including the **Raspberry Pi**, **Teensy-based flight controller**, UART communication link, and remote operation workflow from the **iPad** through the **phone hotspot**.

<p align="center">
  <img src="https://github.com/user-attachments/assets/52606e95-2abf-4574-beb5-166c0522b75b" alt="Full experimental setup" width="85%">
</p>

<p align="center">
  <sub>
    Full setup used for ROS 2-based telemetry monitoring and in-field PID tuning on the UAV platform.
</p>


## 📱 iPad-Based Field Operation

One practical aspect of this project is that the ROS 2 workflow can be operated remotely from an **iPad over SSH**, with both the **iPad** and the **Raspberry Pi** connected to the **phone hotspot** used as the compact field network.

This makes it possible to:

- start the ROS 2 bridge node from a remote terminal;
- monitor live telemetry topics during tests;
- send runtime PID commands without carrying a laptop into the field.

### 🖼️ iPad Screenshots Gallery

<table align="center">
  <tr>
    <td align="center" width="50%">
      <img src="https://github.com/user-attachments/assets/5be3b07b-f35f-4c7b-a213-874deecbb61c" alt="iPad SSH session 1" width="100%"><br>
      <sub><b>📟 SSH Session 1 — Bridge Startup</b></sub><br>
      <sub>Start the ROS 2 UART bridge and verify that <code>/dev/serial0</code> opens correctly.</sub>
    </td>
    <td align="center" width="50%">
      <img src="https://github.com/user-attachments/assets/83e7a21c-6fa3-4ce3-8476-616ccb05a347" alt="iPad SSH session 2" width="100%"><br>
      <sub><b>📡 SSH Session 2 — Telemetry / PID Commands</b></sub><br>
      <sub>Monitor topics, inspect telemetry, and send runtime PID commands during field tests.</sub>
    </td>
  </tr>
</table>


Once the screenshots are available, they can be displayed here as a dedicated gallery or as inline figures below the architecture diagram.

## 🕹️ Operating Logic

The UART channel changes function depending on arm/disarm state and the SWB switch position.

| Condition | UART behavior |
|---|---|
| Armed | Telemetry only |
| Disarmed + SWB up | Telemetry |
| Disarmed + SWB down | PID configuration mode |

This makes it possible to reuse the same serial path for both monitoring and controller editing.

## 📡 ROS Topics

### 📤 Published

| Topic | Type | Description |
|---|---|---|
| `/drone_uart_line` | `std_msgs/msg/String` | Raw UART line |
| `/pid_rx` | `std_msgs/msg/String` | PID/configuration responses from firmware |
| `/pid_tx_echo` | `std_msgs/msg/String` | Echo of transmitted PID commands |
| `/spool_state` | `std_msgs/msg/Int32` | Spool state |
| `/pwr_prop` | `std_msgs/msg/Float32` | Propulsion power term |
| `/roll_rel` | `std_msgs/msg/Float32` | Relative roll angle |
| `/pitch_rel` | `std_msgs/msg/Float32` | Relative pitch angle |
| `/rate_roll_f` | `std_msgs/msg/Float32` | Filtered roll rate |
| `/rate_pitch_f` | `std_msgs/msg/Float32` | Filtered pitch rate |
| `/rate_yaw_f` | `std_msgs/msg/Float32` | Filtered yaw rate |
| `/uroll` | `std_msgs/msg/Float32` | Roll control effort |
| `/upitch` | `std_msgs/msg/Float32` | Pitch control effort |
| `/uyaw` | `std_msgs/msg/Float32` | Yaw control effort |

### 📥 Subscribed

| Topic | Type | Description |
|---|---|---|
| `/pid_cmd` | `std_msgs/msg/String` | Runtime PID/configuration command |

## 🎛️ Runtime Tuning Parameters

### 🔁 Inner Loop (Rate PID)

- `kpr`, `tir`, `tdr`
- `kpp`, `tip`, `tdp`
- `kpy`, `tiy`, `tdy`

### 🧭 Outer Loop

- `kproll`
- `kppitch`

## 💬 UART Interaction Examples

### 📋 Request All Parameters

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'list'}"
```

### 🔍 Read One Parameter

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'get kpr'}"
```

### ✏️ Change One Parameter

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'kpr=0.70'}"
```

### 📬 Read Configuration Responses

```bash
ros2 topic echo /pid_rx std_msgs/msg/String
```

## ⚙️ Requirements

- Ubuntu 22.04 + ROS 2 Humble
- Python 3
- `pyserial`

Install serial support:

```bash
pip3 install pyserial
```

Optional serial-permission tip:

```bash
sudo usermod -a -G dialout $USER
# logout/login if needed
```

## 🛠️ Build (colcon)

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/dev2439/ros2_uav_pid_tuning_bridge.git uart_pid_bridge
cd ..
source /opt/ros/humble/setup.bash
colcon build --packages-select uart_pid_bridge
source install/setup.bash
```

## ▶️ Run

### Option A — Run node directly

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run uart_pid_bridge uart_pid_to_ros
```

### Option B — Run through launch file

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch uart_pid_bridge uart_pid_bridge.launch.py
```

Expected startup message:

```text
[INFO] [...] [uart_pid_bridge_node]: Abriendo UART: /dev/serial0 @ 57600
```

## ✅ Quick Test (2-Session Field Check)

### 1️⃣ Session 1 — Start the Bridge

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run uart_pid_bridge uart_pid_to_ros
```

### 2️⃣ Session 2 — Inspect Topics and Send Commands

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 topic list -t
ros2 topic echo /drone_uart_line
```

Then, when the system is **disarmed** and **SWB is down**:

```bash
ros2 topic pub --once /pid_cmd std_msgs/msg/String "{data: 'list'}"
ros2 topic echo /pid_rx std_msgs/msg/String
```

## 🧪 Recommended Tuning Workflow

1. Power the Raspberry Pi and the Teensy.
2. Start the ROS 2 node in **SSH Session 1**.
3. Use **SSH Session 2** for topic inspection and commands.
4. Confirm telemetry is available.
5. Disarm the vehicle before editing gains.
6. Move **SWB down** to enter PID configuration mode.
7. Read parameters with `list` or `get`.
8. Change a small parameter block.
9. Return to telemetry mode.
10. Perform a short flight and evaluate the response.

A practical rule is to modify **only one parameter group per test** so the effect of each change remains interpretable.

## 💾 Persistence Behavior

Updated gains remain active only while the controller stays powered. After reboot, reset, or firmware reload, the parameters return to the default values compiled in the flight-controller code.

This is useful for experimental work because it preserves a stable baseline after every power cycle.

## 🎯 Use Cases

- UAV controller tuning during early flight tests
- Raspberry Pi ↔ flight-controller middleware integration
- Topic-based telemetry monitoring for debugging
- Field-ready SSH operation from lightweight devices
- Preparation for future logging, dashboards, or supervisory tools

## 🌐 Related Projects

- `Temp_ControlMod_ROS_integration` → similar ROS 2 / UART middleware approach applied to a temperature control module
https://github.com/dev2439/Temp_ControlMod_ROS_integration

## 📝 Notes

- Do not use `miniterm` or another serial terminal at the same time as the ROS 2 bridge on the same UART device.
- The iPad + SSH + hotspot workflow is not mandatory, but it is a practical and compact field setup.
- The node is intentionally simple and focused on rapid controller iteration rather than a large software stack.

## ⚠️ Disclaimer

Educational and experimental use only.
Always follow safe practices when working with UAV propulsion systems.

## 📜 License

MIT License
