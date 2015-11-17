# CVRL FORTH HandTracker


## Description

This script uses the Model Based Vision (MBV) libraries created by the Computer Vision and Robotics Lab at ICS/FORTH. The libraries are free for academic and non-profit use under this [licence](license.txt).

It implements a hand tracker pipeline described first in [Oikonomidis et al: Efficient model-based 3D tracking of hand articulations using Kinect](http://users.ics.forth.gr/~argyros/mypapers/2011_09_bmvc_kinect_hand_tracking.pdf).


The software tracks the 3D position, orientation and full articulation of a human hand from markerless visual observations. The developed method:

 * estimates the full articulation of a hand (26 DoFs redundantly encoded in 27 parameters)  involved in unconstrained motion
 * operates on input acquired by easy-to-install and widely used/supported RGB-D cameras (e.g. Kinect, Xtion)
 * does not require markers, special gloves
 * performs at a rate of 30fps in modern architectures (GPU acceleration)
 * does not require calibration
 * does not rely on any proprietary built-in tracking technologies (Nite, OpenNI, Kinect SDK)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=Fxa43qcm1C4" target="_blank"><img src="http://img.youtube.com/vi/Fxa43qcm1C4/0.jpg" alt="Single hand tracking" width="320" height="240" border="10"/></a>


## Hardware Requirements

System requirements:

- Hardware
	- Multi-core Intel CPU
	- 1 GB of RAM or more
	- CUDA-enabled GPU
		- 512MB GPU RAM or more
		- CUDA compute capability > 1.0
		- OpenGL 3.3
- Software
	- OS
		- 64bit Windows 8 or newer
		- 64bit Ubuntu 14.04 Linux
	- Environment
		- **Python 2.7 64bit**
	- Drivers
		- [Latest CUDA driver](https://developer.nvidia.com/cuda-downloads)
		- OpenNI driver
		- Kinect 2 driver

## Download links
<a name="download"></a>

- [Ubuntu 3D hand tracking](http://cvrlcode.ics.forth.gr/files/mbv/v1.1/MBV_PythonAPI_Linux_1.1.zip)
- [Windows 3D hand tracking](http://cvrlcode.ics.forth.gr/files/mbv/v1.1/MBV_PythonAPI_Win_1.1.zip)

### Windows Dependencies

- [Visual C++ **64bit** Redistributable Packages for Visual Studio 2013](https://www.microsoft.com/en-us/download/details.aspx?id=40784)
- [OpenNI 1.x SDK for Windows 8 **64bit** and newer](http://cvrlcode.ics.forth.gr/web_share/OpenNI/OpenNI_SDK/OpenNI_1.x/OpenNI-Win64-1.5.7.10-Dev.zip) (install prior to sensor driver)
- [OpenNI 1.x sensor driver for 8 Windows **64bit** and newer](http://cvrlcode.ics.forth.gr/web_share/OpenNI/OpenNI_SDK/OpenNI_1.x/Sensor_Driver/Sensor-Win64-5.1.6.6-Redist.zip)
- [Kinect 2 SDK for Windows 8 **64bit** and newer](http://www.microsoft.com/en-us/download/details.aspx?id=44561)

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

The provided package has some external dependencies, listed below. One such dependency is a working Python 2.7 environment.

<span style="color:#FFFFFF;background-color:#FF0000">**Notice:**</span> Make sure the Python version is 2.7 64bit.

<span style="color:#FFFFFF;background-color:#FF0000">**Notice:**</span> Binaries were build against CUDA 7.5. This might require the user to update the GPU driver to the latest version. In the lack of a supported driver, an error message of the form "*CUDA driver version is insufficient for CUDA runtime version*" is issued.

### Ubuntu

Install opencv, thread building blocks (TBB) python and numpy by executing the following in the command line:

```
sudo apt-get install libopencv-dev libtbb2 python-numpy python-opencv
```

If you plan to use openni1.x (required for running some of the example scripts), also execute:

```
sudo apt-get install libopenni0 libopenni-sensor-primesense0 
```

Make sure that you have nvidia driver 352 or newer installed. Use the
"Additional Drivers" tool to select the correct driver version.

### Windows

OpenCV is statically built with the provided binaries. Thread building blocks is bundled with the downloadable package. The rest of the dependencies should be downloaded from the download section. For python support it is suggested to use [anaconda] (https://www.continuum.io/downloads). After installing Anaconda, the installation of numpy is a simple as executing the following in the command line:

```
conda install numpy
```

<span style="color:#FFFFFF;background-color:#FF0000">**Notice:**</span> Binaries were built against numpy 1.10.1. If a numpy related error (import or other) is issued, updating numpy to this version will be required. In Anaconda it would suffice to execute the following, from the command line:

```
conda update numpy
```

### Usage

Make sure the current working directory is the root of HandTracker and that <tt>MBV_LIBS</tt> is set.

Run the `runme.sh` (Ubuntu) or `runme.bat` (Windows) script to test the hand tracker. Press `s` to stop/start 3D hand tracking.

<span style="color:#FFFFFF;background-color:#FF0000">**Notice:**</span> Be aware that the first execution will take a significant amount of time, CPU and memory. This is due to the intermediate CUDA code being compiled. This will only happen once, as the compilation result is cached. In Ubuntu the cache limit might be too restricting and in these cases caching will fail, leading to recompilation at every execution. To remedy this the size can be increased as follows (command line):

```
export CUDA_CACHE_MAXSIZE=2147483648
```


## Contact

For questions, comments and any kind of feedback please use the github issues, and the wiki. 

