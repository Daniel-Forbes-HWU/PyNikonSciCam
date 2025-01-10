import cv2
import matplotlib.pyplot as plt
from PyNikonSciCam import NikonCamera

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
