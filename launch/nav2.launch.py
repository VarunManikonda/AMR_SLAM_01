import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('my_amr')
    nav2_bringup = get_package_share_directory('nav2_bringup')

    map_file = os.path.join(pkg, 'maps', 'my_map.yaml')
    params_file = os.path.join(pkg, 'config', 'nav2_params.yaml')

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'map': map_file,
            'params_file': params_file,
        }.items()
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(
            nav2_bringup, 'rviz', 'nav2_default_view.rviz')],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        nav2,
        rviz,
    ])
