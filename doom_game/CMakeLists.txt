cmake_minimum_required(VERSION 3.10)
project(DoomGame)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(SDL2 REQUIRED)

include_directories(${SDL2_INCLUDE_DIRS})

add_executable(DoomGame src/main.cpp)
target_link_libraries(DoomGame ${SDL2_LIBRARIES})
