import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import OpaqueFunction, IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

def launch_setup(context, *args, **kwargs):

    world = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'worlds', 'turtlebot3_world.world')
    
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    nav2_file_dir = get_package_share_directory('turtlebot3_navigation2')
    gazebo_launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    cartographer_launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_cartographer'), 'launch')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')

    param_file_name = TURTLEBOT3_MODEL + '.yaml'

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose
        }.items()
    )

    cartographer_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(cartographer_launch_file_dir, 'cartographer.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    nav2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_file_dir, 'launch', 'navigation2.launch.py')
        ),
        launch_arguments={
            'map': os.path.join(nav2_file_dir, 'map', 'map.yaml'),
            'use_sim_time': use_sim_time,
            'params_file': os.path.join(nav2_file_dir, 'param', param_file_name)}.items(),
    )
    demo_cmd = Node(
        package='py_launch_example',
        executable='demo_sweep',
        emulate_tty=True,
        output='screen',
    )


    return [
        gzserver_cmd,
#        gzclient_cmd,
        robot_state_publisher_cmd,
        spawn_turtlebot_cmd,
        cartographer_cmd,
        nav2_cmd,
#	demo_cmd,
    ]


def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])
