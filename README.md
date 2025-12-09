# MAVEN Data Supplementary Toolkit 
## Overview
This repository provides four IDL programs (built on the SPEDAS library) and one Python script designed to simplify accessing, downloading, and processing MAVEN mission data.
## Contents
| Name                 | Description |
|----------------------|-------------|
| [maven_data_tplot](https://github.com/StellarPlasma/MAVEN_IDL/blob/main/maven_data_tplot.pro)     |Download, read, and process data from multiple MAVEN instruments using a single-line command. This script integrates multiple instrument-specific SPEDAS routines.|
| [maven_orbit_track](https://github.com/StellarPlasma/MAVEN_IDL/blob/main/maven_orbit_track.pro)    |Retrieve MAVEN orbit information as well as plasma and magnetic field measurements based on user-defined search criteria.|
| [mvn_mag_zenith_angle](https://github.com/StellarPlasma/MAVEN_IDL/blob/main/mvn_mag_zenith_angle.pro) |Compute the angle between the local magnetic field vector at MAVEN and the radial (vertical) vector pointing outward from Mars.|
| [tplot_consult](https://github.com/StellarPlasma/MAVEN_IDL/blob/main/tplot_consult.pro)        |Extract the value of a specified tplot variable at a given timestamp.|
| [mvn_data_downloader](https://github.com/StellarPlasma/MAVEN_IDL/blob/main/mvn_data_downloader.py)       |Download Maven data from the Berkeley or LASP servers|
## Usage
### IDL Scripts
The IDL programs require a working installation of **IDL** and **SPEDAS**.
To install SPEDAS, please refer to the [SPEDAS wiki](http://spedas.org/wiki/index.php?title=Main_Page). Example calling sequences for each IDL program are provided in the header documentation of each file.
### Python Script
The Python script [mvn_data_downloader.py](https://github.com/StellarPlasma/MAVEN_IDL/blob/main/mvn_data_downloader.py) can be executed directly from any Python environment (e.g., Spyder).
On Windows systems, it requires a local installation of the [wget](https://eternallybored.org/misc/wget/) executable.
