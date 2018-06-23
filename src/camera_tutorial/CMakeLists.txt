cmake_minimum_required(VERSION 2.8)
project(image_transport_tutorial)
add_compile_options(-std=c++11)
find_package(catkin REQUIRED COMPONENTS  cv_bridge std_msgs image_transport message_generation sensor_msgs geometry_msgs camera_info_manager)

# add the resized image message
add_message_files(
   FILES
   tracking2Dmsg.msg
)
generate_messages(DEPENDENCIES std_msgs sensor_msgs geometry_msgs)

catkin_package(CATKIN_DEPENDS cv_bridge  image_transport message_runtime std_msgs sensor_msgs geometry_msgs)

find_package(OpenCV)

include_directories(include ${catkin_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})

# add the publisher example
add_executable(my_publisher src/my_publisher.cpp)
add_dependencies(my_publisher ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})
target_link_libraries(my_publisher ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})

# add the subscriber example
add_executable(my_subscriber src/my_subscriber.cpp)
add_dependencies(my_subscriber ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})
target_link_libraries(my_subscriber ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})

#for pos_xy_analysis
add_executable(angle_pos_sub src/angle_pos_sub.cpp)
add_dependencies(angle_pos_sub ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})
target_link_libraries(angle_pos_sub ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})

# add the plugin example
# add_library(resized_publisher src/manifest.cpp src/resized_publisher.cpp src/resized_subscriber.cpp)
# add_dependencies(resized_publisher ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})
# target_link_libraries(resized_publisher ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})


# Mark executables and/or libraries for installation
install(TARGETS my_publisher my_subscriber angle_pos_sub #resized_publisher
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# install(FILES resized_plugins.xml
#         DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
# )
