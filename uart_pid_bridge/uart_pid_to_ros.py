#!/usr/bin/env python3
"""ROS 2 UART bridge for UAV telemetry and runtime PID tuning."""

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Int32, String
import serial

PORT = '/dev/serial0'
BAUD = 57600
READ_TIMEOUT_S = 0.02
TIMER_PERIOD_S = 0.01
EXPECTED_TELEMETRY_FIELDS = 10


class UartPidBridge(Node):
    """Bridge UART telemetry and ASCII PID commands into ROS 2 topics.

    Expected telemetry CSV format:
        spool,PwR,roll_rel,pitch_rel,RateRoll_f,RatePitch_f,RateYaw_f,Uroll,Upitch,Uyaw\n
    Expected configuration responses:
        OK kpr=0.700000
        ERR unknown_param
        MODE PID_CONFIG
    """

    def __init__(self) -> None:
        super().__init__('uart_pid_bridge_node')

        # Raw UART and command topics
        self.pub_line = self.create_publisher(String, 'drone_uart_line', 20)
        self.pub_pid_rx = self.create_publisher(String, 'pid_rx', 20)
        self.pub_pid_tx_echo = self.create_publisher(String, 'pid_tx_echo', 20)

        # Parsed telemetry topics
        self.pub_spool = self.create_publisher(Int32, 'spool_state', 10)
        self.pub_pwr = self.create_publisher(Float32, 'pwr_prop', 10)
        self.pub_roll = self.create_publisher(Float32, 'roll_rel', 10)
        self.pub_pitch = self.create_publisher(Float32, 'pitch_rel', 10)
        self.pub_rr = self.create_publisher(Float32, 'rate_roll_f', 10)
        self.pub_rp = self.create_publisher(Float32, 'rate_pitch_f', 10)
        self.pub_ry = self.create_publisher(Float32, 'rate_yaw_f', 10)
        self.pub_ur = self.create_publisher(Float32, 'uroll', 10)
        self.pub_up = self.create_publisher(Float32, 'upitch', 10)
        self.pub_uy = self.create_publisher(Float32, 'uyaw', 10)

        self.sub_pid_cmd = self.create_subscription(
            String, 'pid_cmd', self.on_pid_cmd, 10
        )

        self.get_logger().info(f'Abriendo UART: {PORT} @ {BAUD}')
        self.ser = serial.Serial(PORT, BAUD, timeout=READ_TIMEOUT_S)
        time.sleep(0.2)

        self.timer = self.create_timer(TIMER_PERIOD_S, self.timer_callback)

    def on_pid_cmd(self, msg: String) -> None:
        """Send ASCII commands received from ROS 2 into the UART link."""
        cmd = msg.data.strip()
        if not cmd:
            return

        if not cmd.endswith('\n'):
            cmd += '\n'

        try:
            self.ser.write(cmd.encode())
            echo = String()
            echo.data = cmd.strip()
            self.pub_pid_tx_echo.publish(echo)
            self.get_logger().info(f'UART TX -> {cmd.strip()}')
        except Exception as exc:
            self.get_logger().error(
                f'Error sending PID command through UART: {exc}'
            )

    def timer_callback(self) -> None:
        """Read UART lines, classify them, and publish ROS topics."""
        line = self.ser.readline()
        if not line:
            return

        try:
            text = line.decode(errors='replace').strip()
        except Exception:
            return

        if not text:
            return

        raw_msg = String()
        raw_msg.data = text
        self.pub_line.publish(raw_msg)

        # ASCII configuration responses
        if (
            text.startswith('OK ')
            or text.startswith('ERR ')
            or text.startswith('MODE ')
            or text.startswith('k')
            or text.startswith('t')
        ):
            self.pub_pid_rx.publish(raw_msg)
            return

        # CSV telemetry frame
        parts = text.split(',')
        if len(parts) != EXPECTED_TELEMETRY_FIELDS:
            return

        try:
            spool = int(float(parts[0]))
            values = [float(x) for x in parts[1:]]
        except ValueError:
            return

        spool_msg = Int32()
        spool_msg.data = spool
        self.pub_spool.publish(spool_msg)

        publishers = [
            self.pub_pwr,
            self.pub_roll,
            self.pub_pitch,
            self.pub_rr,
            self.pub_rp,
            self.pub_ry,
            self.pub_ur,
            self.pub_up,
            self.pub_uy,
        ]

        for publisher, value in zip(publishers, values):
            msg = Float32()
            msg.data = value
            publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = UartPidBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.ser.close()
        except Exception:
            pass
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
