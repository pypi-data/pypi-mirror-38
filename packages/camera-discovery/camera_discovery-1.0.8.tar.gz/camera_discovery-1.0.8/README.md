# Camera Discovery
This is a package to discover all onvif devices on your network.
## Installation
Install the package through pip:
````
pip install camera-discovery
````
## Execution
To execute the command that discover all cameras:
````
from camera_discovery import CameraDiscovery
CameraDiscovery.ws_discovery()
````
To execute the comand that shows information about the cameras:
from camera_discovery import CameraONVIF
Class = CameraONVIF(camera_ip, user, password)