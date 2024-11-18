#
# Copyright 2024 pinorobotics
#
# Website: https://github.com/pinorobotics/r2d2_urdf
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from launch import LaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
  share_folder = FindPackageShare('r2d2_urdf')
  use_gui = LaunchConfiguration("use_gui")
  robot_description_content = Command(
      [
          PathJoinSubstitution([FindExecutable(name="xacro")]),
          " ",
          PathJoinSubstitution([share_folder, "urdf", "Dorna2.urdf"]),
      ])
  robot_description = {"robot_description": ParameterValue(robot_description_content, value_type=str)}
  rviz_config_file = PathJoinSubstitution([share_folder, "rviz", "demo.rviz"])
  return LaunchDescription([
      # robot_state_publisher
      Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description]),
      Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]),
      Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[{"source_list": ["dorna2_joint_states"]}],
        condition=UnlessCondition(use_gui)),
      Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(use_gui))
    ])
