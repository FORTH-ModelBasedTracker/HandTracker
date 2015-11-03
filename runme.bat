@echo off
echo "MBV_LIBS Environment variable should point to the MBV libraries folder."
echo "MBV_LIBS" %MBV_LIBS%
echo "Setting PATH and PYTHONPATH"
set PATH=%MBV_LIBS\libs%;%PATH%
set PYTHONPATH=%MBV_LIBS%\python_libs;%PYTHONPATH%

echo "Running the Single Hand Tracker script..."
python src\SingleHandTracking.py