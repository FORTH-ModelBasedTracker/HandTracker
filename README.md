# HandTracker

Python scripts implementing the hand tracker pipeline released on github.

## Description

This script uses the Model Based Vision (MBV) libraries created by the Computer Vision and Robotics Lab at ICS/FORTH. The libraries are free for academic and non-profit use under this [licence](licence.txt).

It implements a hand tracker pipeline described first in [Oikonomidis et al: Efficient model-based 3D tracking of hand articulations using Kinect](http://users.ics.forth.gr/~argyros/mypapers/2011_09_bmvc_kinect_hand_tracking.pdf).

The software tracks the 3D position, orientation and full articulation of a human hand from markerless visual observations. The developed method:

 * estimates the full articulation of a hand (26 DoFs)  involved in unconstrained motion
 * operates on input acquired by easy-to-install and widely used/supported RGB-D cameras (e.g. Kinect, Xtion)
 * does not require markers, special gloves
 * performs at a rate of 20fps in modern architectures (GPU acceleration)
 * does not require calibration
 * does not rely on any proprietary built-in tracking technologies (Nite, OpenNI, Kinect SDK)

## Hardware Requirements

System requirements:
 - PC with at least 1 GB of RAM
 - 64bit Windows 10 or 64bit Ubuntu 14.04 Linux
 - CUDA enabled GPU card (Compute Capability 1.0 and newer) with 256 ΜΒ of RAM


## Dependencies

The MBV libraries depend on [OpenCV 2.4](http://opencv.org/) and [tbb 4.2](https://www.threadingbuildingblocks.org/).

Additionally the python libs use python2.7 and numpy.

Linux users just install them using apt:

```
sudo apt-get install libopencv-dev libtbb2 python-numpy
```

Windows users must first download and install the correct versions from the links above. For the python packages it is suggested to use [anaconda] (https://www.continuum.io/downloads) which comes with many extra packages including numpy.

In order to use the example script you need to install OpenNI1.x to your system. You will also need a Xtion or Kinect RGBD sensor to use it in real time. You can download the OpenNI1.x binaries and Xtion drivers from [here](http://cvrlcode.ics.forth.gr/web_share/OpenNI/OpenNI_SDK/OpenNI_1.x).

## Usage

To run the hand tracker script you need to download for [Ubuntu 14.04 64](http://cvrlcode.ics.forth.gr/files/mbv/v1.0/MBV_PythonAPI_1.0.zip) or [Windows10 64](http://cvrlcode.ics.forth.gr/files/mbv/v1.0/MBV_PythonAPI_1.0.zip) the MBV and HandTracker libraries for your system. 

Unzip the package and set an environment variable named *MBV_SDK* to point to the location of the libraries. The runme scripts use the *MBV_SDK* variable to setup the library paths and python paths correctly before running the script.

You are done. Run the `runme.sh` or `runme.bat` script to test the hand tracker. 

Happy Tracking! :) 


## Contact

For questions, comments and any kind of feedback please use the github issues, and the wiki. 


