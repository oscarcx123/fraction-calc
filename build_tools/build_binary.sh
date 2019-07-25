#!/bin/sh
python3 setup.py build_ext --inplace
gcc main.c -I/usr/include/python3.7m/ -L/usr/lib/libpython3.7m.so -lpython3.7m  -o fractionCalc