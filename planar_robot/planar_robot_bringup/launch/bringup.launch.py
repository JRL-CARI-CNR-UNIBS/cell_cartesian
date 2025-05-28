
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription,ExecuteProcess 
from launch_ros.substitutions import FindPackageShare
from launch.actions import GroupAction, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
from launch.conditions import IfCondition, UnlessCondition

import os
import xacro

def generate_launch_description():

    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "use_gazebo",
            default_value="false",
            description="Start Gazebo.",
        )
    )

    use_gazebo = LaunchConfiguration("use_gazebo")
    description_package='planar_robot_description'
    description_file='planar_robot.xacro'
    moveit_config_package='planar_robot_moveit_config'
    moveit_config_file='cartesian_cell.srdf'
    moveit_controllers_file='moveit_controllers.yaml'
    controllers_file='ros2_controllers.yaml'
    initial_joint_controller='faulty_velocity_controller'
    runtime_config_package='planar_robot_bringup'
    launch_rviz='false'

    control_launcher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('planar_robot_bringup'),'launch', 'control.launch.py')]),
        launch_arguments={
            'use_gazebo': use_gazebo,
            'description_package': description_package,
            'description_file': description_file,
            'launch_rviz': launch_rviz,
            'moveit_config_package': moveit_config_package,
            'runtime_config_package': runtime_config_package,
            'controllers_file': controllers_file,
            'initial_joint_controller': initial_joint_controller
        }.items(),
    )

    moveit_launcher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('planar_robot_bringup'),'launch', 'moveit.launch.py')]),
        launch_arguments={
            'use_gazebo': use_gazebo,
            'robot_xacro_file': description_file,
            'support_package': description_package,
            'moveit_config_package': moveit_config_package,
            'moveit_config_file': moveit_config_file,
            'moveit_controllers_file': moveit_controllers_file
        }.items()
    )
    
    # Start Gazebo
    gazebo_launcher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('planar_robot_bringup'),'launch', 'gazebo_world.launch.py')]),
#        launch_arguments={
#            'robot_xacro_file': description_file,
#            'support_package': description_package,
#            'moveit_config_package': moveit_config_package,
#            'moveit_config_file': moveit_config_file,
#            'moveit_controllers_file': moveit_controllers_file
#        }.items(),
        condition=IfCondition(use_gazebo),
    )

    nodes_to_start = [
        control_launcher,
        moveit_launcher,
        gazebo_launcher,
    ]

    return LaunchDescription( declared_arguments + nodes_to_start)

