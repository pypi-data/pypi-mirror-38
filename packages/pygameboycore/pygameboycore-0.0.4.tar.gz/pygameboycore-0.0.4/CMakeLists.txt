cmake_minimum_required(VERSION 2.8.12)

project(pygameboycore)

set(BUILD_TESTS OFF)
set(BUILD_TOOLS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(SOURCE_DIR "src/pygameboycore")

add_subdirectory(lib/gameboycore)
add_subdirectory(lib/pybind11)

find_package(PythonLibs REQUIRED)
include_directories(${SOURCE_DIR} ${PYTHON_INCLUDE_DIRS})
include_directories("lib/gameboycore/src/gameboycore/include")

pybind11_add_module(pygameboycore ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
target_link_libraries(pygameboycore PRIVATE gameboycore)
