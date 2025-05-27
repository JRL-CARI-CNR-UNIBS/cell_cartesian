cmake_minimum_required(VERSION 3.10.2)

project(planar_robot_bringup)

find_package(ament_cmake REQUIRED)

ament_package()

install(DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME})
