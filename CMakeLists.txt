cmake_minimum_required(VERSION 3.10)
project(stypuff)
set(CMAKE_CXX_STANDARD 17)

# Source files
add_executable(stypuff
    stypuffheart.cc
)

target_include_directories(stypuff PRIVATE ${CMAKE_SOURCE_DIR})
