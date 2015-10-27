#!/bin/bash
echo "MBV_SDK Environment variable should point to the MBV libraries folder."
echo "MBV_SDK" $MBV_SDK
echo "Setting LD_LIBRARY_PATH and PYTHONPATH"
export LD_LIBRARY_PATH=$MBV_SDK/libs:$LD_LIBRARY_PATH
export PYTHONPATH=$MBV_SDK/python_libs:$PYTHONPATH

echo "Running the Single Hand Tracker script..."
python src/SingleHandTracking.py
