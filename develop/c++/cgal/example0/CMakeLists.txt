set("CMAKE_BUILD_TYPE" "Release")
cmake_minimum_required(VERSION 3.10)
project(CGALExample)

find_package(CGAL REQUIRED)

add_executable(CGALExample main.cpp)
target_link_libraries(CGALExample CGAL::CGAL)

