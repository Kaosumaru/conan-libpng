PROJECT(MyHello)
cmake_minimum_required(VERSION 3.0)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(pngtest pngtest.cpp)

TARGET_LINK_LIBRARIES(pngtest ${CONAN_LIBS})
