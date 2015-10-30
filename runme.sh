#!/bin/bash
echo "MBV_LIBS Environment variable should point to the MBV libraries folder."
echo "MBV_LIBS" $MBV_LIBS
echo "Setting LD_LIBRARY_PATH and PYTHONPATH"
export LD_LIBRARY_PATH=$MBV_LIBS/libs:$LD_LIBRARY_PATH
export PYTHONPATH=$MBV_LIBS/python_libs:$PYTHONPATH

echo "Running the Single Hand Tracker script..."
python src/SingleHandTracking.py
