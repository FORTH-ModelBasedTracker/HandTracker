# HandTracker

Python scripts implementing the hand tracker pipeline released on github.

## Description

<a href="http://www.youtube.com/watch?feature=player_embedded&v=Fxa43qcm1C4" target="_blank" align="right"><img src="http://img.youtube.com/vi/Fxa43qcm1C4/0.jpg" alt="Single hand tracking" width="240" height="180" border="10" align="right" /></a> 

This script uses the Model Based Vision (MBV) libraries created by the Computer Vision and Robotics Lab at ICS/FORTH. The libraries are free for academic and non-profit use under this [licence](licence.txt).

It implements a hand tracker pipeline described first in [Oikonomidis et al: Efficient model-based 3D tracking of hand articulations using Kinect](http://users.ics.forth.gr/~argyros/mypapers/2011_09_bmvc_kinect_hand_tracking.pdf).


The software tracks the 3D position, orientation and full articulation of a human hand from markerless visual observations. The developed method:

 * estimates the full articulation of a hand (26 DoFs)  involved in unconstrained motion
 * operates on input acquired by easy-to-install and widely used/supported RGB-D cameras (e.g. Kinect, Xtion)
 * does not require markers, special gloves
<a href="http://www.youtube.com/watch?feature=player_embedded&v=e3G9soCdIbc" target="_blank" align="right"><img src="http://img.youtube.com/vi/e3G9soCdIbc/0.jpg" alt="Two hand tracking" width="240" height="180" border="10" align="right" /></a> 
 * performs at a rate of 20fps in modern architectures (GPU acceleration)
 * does not require calibration
 * does not rely on any proprietary built-in tracking technologies (Nite, OpenNI, Kinect SDK)

## Hardware Requirements

System requirements:

- Hardware
	- Multi-core CPU *(Intel? AMD?)*
	- 1 GB of RAM or more
	- CUDA-enabled GPU (compute capability > 1.0)
		- 512MB GPU RAM or more
- Software
	- OS
		- 64bit Windows 8 or newer
		- 64bit Ubuntu 14.04 Linux
	- Drivers
		- Latest CUDA driver
		- OpenNI driver (only if OpenNI acquisition will be used)
		- Kinect 2 driver (Windows 8 or newer, only if Kinect2 acquisition will be used)

## Download links
<a name="download"></a>

- 3D Hand tracking
	- [Ubuntu 3D hand tracking](http://cvrlcode.ics.forth.gr/files/mbv/v1.0/MBV_PythonAPI_1.0.zip)
	- [Windows 3D hand tracking](http://cvrlcode.ics.forth.gr/files/mbv/v1.0/MBV_PythonAPI_1.0.zip)

## Installation and usage

As a first step, download the package that matches your OS from [the download section](#download). Extract the downloaded package to a location and set an environment variable named <tt>MBV_LIBS</tt> to point to this location. For example, if the package is extracted to the path <tt>c:\Users\User\Documents\FORTH\HANDTRACKER</tt> (Windows) or <tt>/home/user/FORTH/HANDTRACKER</tt> (Ubuntu), do the following from the command line:


Ubuntu:

```
export MBV_LIBS=/home/user/FORTH/HANDTRACKER
```

Windows:

```
set MBV_LIBS=c:\Users\User\Documents\FORTH\HANDTRACKER
```

### Ubuntu

Install opencv, thread building blocks (TBB) python and numpy by executing the following in the command line:

```
sudo apt-get install libopencv-dev libtbb2 python-numpy
```

If you plan to use openni1.x (required for running some of the example scripts), also execute:

```
sudo apt-get install libopenni0 libopenni-sensor-primesense0 
```

### Windows

OpenCV is statically built with the provided binaries. Thread building blocks can be found in the 3rd party library binaries of [the download section](#download). The same holds for the required OpenNI and Kinect 2 SDKs. For python support it is suggested to use [anaconda] (https://www.continuum.io/downloads). After installing Anaconda, the installation of numpy is a simple as executing the following in the command line:

```
conda install numpy
```



### Usage

Make sure the current working directory is the root of HandTracker. Also make sure to have a working installation of OpenNI 1.x (SDK and drivers).

Run the `runme.sh` (Ubuntu) or `runme.bat` (Windows) script to test the hand tracker. Press `s` to stop/start 3D hand tracking.


## Contact

For questions, comments and any kind of feedback please use the github issues, and the wiki. 

