from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition
from ament_index_python import get_package_share_directory
from launch.actions import IncludeLaunchDescription,ExecuteProcess 
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os


def generate_launch_description():
    declared_arguments = []
    
    world_path = os.path.join(
        get_package_share_directory('planar_robot_description'),
        'models', 'world', 'minimal_world.sdf'
    )

    #world_path_hardcoded = "/home/galileo/projects/merlin2_ws/src/cell_cartesian/planar_robot/planar_robot_description/models/world/minimal_world.sdf"


    gazebo = ExecuteProcess(
        cmd=["ign", "gazebo", "-r", "-v", "4", world_path   ], #  
        output="screen"
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "planar_robot",
            "-topic", "robot_description",
            "-x", "0", "-y", "0", "-z", "0"
        ],
        output="screen"
    )
    
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='clock_bridge',
        arguments=[
            '/world/default/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
        ],
        remappings=[
            ('/world/default/clock', '/clock')
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    
    return LaunchDescription(declared_arguments + [
        gazebo,
        clock_bridge,
        spawn_entity,
    ])