#-------------------------------------------------
#
# Project created by QtCreator 2019-12-30T22:39:22
#
#-------------------------------------------------

QT       -= gui

TARGET = dcontinpals
TEMPLATE = lib

DEFINES += DCONTINPALS_LIBRARY

SOURCES += dcontinpals.cpp\
CONTINPALS/CONTPALS.FOR

HEADERS += dcontinpals.h\
        dcontinpals_global.h

LIBS += -lgfortran
LIBS += -static-libgcc -static-libstdc++

unix {
    target.path = /usr/lib
    INSTALLS += target
}
