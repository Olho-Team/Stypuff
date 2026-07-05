cmake_minimum_required(VERSION 3.10)
project(stypuff)
set(CMAKE_CXX_STANDARD 17)

# Source files (adjust if more files are added)
add_executable(stypuff
    stypuffheart.cc
    localdata.cc
    branch.cc
)

target_include_directories(stypuff PRIVATE ${CMAKE_SOURCE_DIR})
