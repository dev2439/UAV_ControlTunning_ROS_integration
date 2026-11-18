from setuptools import find_packages, setup

package_name = 'uart_pid_bridge'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/uart_pid_bridge.launch.py']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Cristian Castro Lagos',
    maintainer_email='replace_with_your_email@example.com',
    description='ROS 2 UART bridge for UAV telemetry monitoring and runtime PID tuning.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'uart_pid_to_ros = uart_pid_bridge.uart_pid_to_ros:main',
        ],
    },
)
