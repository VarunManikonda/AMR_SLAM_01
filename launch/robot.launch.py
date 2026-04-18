import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg = get_package_share_directory('my_amr')
    urdf_file = os.path.join(pkg, 'urdf', 'robot.urdf.xacro')
    world_file = os.path.join(pkg, 'worlds', 'empty_world.sdf')

    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch', 'gz_sim.launch.py'
            )
        ),
        launch_arguments={'gz_args': '-r ' + world_file}.items()
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_amr',
            '-topic', 'robot_description',
            '-x', '0', '-y', '0', '-z', '0.05'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg, 'config', 'bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local'
        }],
        output='screen'
    )

    return LaunchDescription([
        gz_sim,
        rsp,
        spawn,
        bridge,
    ])