# Field Workflow and System Context

This note summarizes the practical operating context behind the ROS 2 UART PID bridge.

## Purpose

The package was created to support **rapid controller tuning during UAV flight tests** without recompiling firmware between every gain modification.

The serial link between the Raspberry Pi and the Teensy is reused dynamically depending on the vehicle state:

- **telemetry mode** during normal monitoring or flight;
- **PID configuration mode** while the system is disarmed.

## Hardware and network arrangement

A typical field deployment uses:

- a **Teensy** running the flight controller firmware;
- a **Raspberry Pi** running ROS 2 and the UART bridge node;
- a **UART** physical link between both devices;
- an **iPad** used as a remote SSH client;
- a **phone hotspot** providing a compact local Wi-Fi network.

This setup avoids carrying a full laptop while still keeping the tuning loop interactive.

## Two-terminal operation

The recommended workflow uses two SSH sessions:

### Session 1

Used exclusively to run the ROS 2 node.

### Session 2

Used to:

- inspect topics;
- observe telemetry;
- send runtime PID commands;
- validate responses.

Keeping the node and the operator commands in separate terminals makes field operation simpler and more reliable.

## Serial behavior

| Vehicle / switch state | Serial behavior |
|---|---|
| Armed | telemetry |
| Disarmed + SWB up | telemetry |
| Disarmed + SWB down | PID configuration |

This logic ensures that the same serial channel can support both observation and configuration without adding another communication interface.

## Why ROS 2 here?

ROS 2 acts as a practical middleware layer between the embedded controller and the operator. In this project it is used for:

- clean topic-based access to telemetry;
- command publication through standard ROS messages;
- fast terminal-based interaction from a remote device;
- future extensibility toward logging, dashboards, or more advanced tooling.

## Experimental philosophy

The bridge is not meant to replace the onboard controller. Instead, it supports the **outer workflow of testing**:

1. inspect telemetry;
2. change a small set of gains;
3. test again;
4. compare behavior;
5. converge toward a better controller.

This is especially useful during early-stage UAV development, where the operator needs a lightweight but structured way to iterate on control parameters in real conditions.
