# PyNikonSciCam Camera Interface

A Python wrapper for controlling Nikon scientific cameras through the Nikon SDK. This library provides a high-level interface for camera control and image acquisition.

## Supported Cameras

- Nikon DS-Fi3
- Nikon DS-Ri2/DS-Qi2 (SDK compatible but untested)
- Digital Sight 10 (SDK compatible but untested)

## Prerequisites

### SDK Installation

1. Create an account at [NISDK](https://nisdk.recollective.com/microscopes)
2. Wait for registration confirmation (typically several days)
3. Download the SDK for Nikon DS-Fi3 from the website
4. Request password to unzip the SDK by emailing: nisdk.us@nikon.com (It may take several days before they respond back with a password.)
5. Install the SDK on your system

The SDK documentation can be found at: `C:\Program Files\Nikon\DSCamSDK\Help\DSCamAPI-E.chm`

The SDK provides a sample application, use this to verify the camera is connected and working correctly.

### Python Requirements

- Python 3.7 or higher
- NumPy

## Installation

1. Clone this repository
2. Install the package using pip:
    
    `pip install .\dist\PyNikonSciCam-x.x.x-py3-none-any.whl`
    - Substituting the x's above with the latest version number available.
 
3. Copy the SDK's DLL `DSCam.dll` into the directory of the pip installed package. E.g.: 

    "C:\Users\MyUSER\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyNikonSciCam"
    - Substituting the Python version and user name as appropriate (example above for Python 3.11).

## Quick Start

Here's a minimal example to capture an image:

```Python
from PyNikonSciCam import NikonCamera
import cv2
import matplotlib.pyplot as plt

# Initialize camera
camera = NikonCamera(3)  # ID = 0 for camera. ID = 3 for simulator

# Capture image
image = camera.get_image()

# Display image using OpenCV
cv2.imshow('Captured Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Optionally, display image using matplotlib
# plt.imshow(image)
# plt.show()
```

## Limitations

Current limitations of the library include:

- Only able to take single images, video streaming is not implemented
- Image format is hardcoded to RGB24 with 2880x2048 resolution
- Only supports Windows operating systems (due to SDK limitations)
- Limited error handling for camera disconnection scenarios
- No support for concurrent camera access


## Contributors
- [@Johan van der Westhuizen](https://github.com/JohanvdWesthuizen)
- [@Dan Forbes](https://github.com/Daniel-Forbes-HWU)
- [@Kees van der Oord](https://github.com/Kees-van-der-Oord-Nikon)


## Building
  1. Install the build tools with: `pip install -U build`
  2. Increment the version number in the "pyproject.toml" file. Then run the following command in the root directory of the project. 
  3. Run the following command in the root directory of the project: `python -m build`
  4. The wheel file will be created in the "dist" directory.
