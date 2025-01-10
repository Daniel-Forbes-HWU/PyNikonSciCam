from PyNikonSciCam import NikonCamera, ECamFeatureId, ECamFormatColor, ECamFormatSize
import matplotlib.pyplot as plt


def main():
    # Initialize the camera
    # camera = NikonCamera()
    # # ...
    # camera.disconnect()

    # ID = 0 for camera connected to the computer
    # ID = 3 for simulator
    with NikonCamera(0, set_defaults=True) as camera:

        # Set the exposure time
        new_exposure_time = 70000
        camera.set_feature_value(ECamFeatureId.ExposureTime, new_exposure_time)


        # Set Gain
        new_gain = 100
        camera.set_feature_value(ECamFeatureId.Gain, new_gain)
        print(f" Gain: {camera.get_feature_value(ECamFeatureId.Gain, update_map=True)}")

        # For White Balance, only Red and Blue can be set.
        # The settable range is between 0 and 799 at 1 step interval, for each color.
        # Set White Balance Red value
        white_balance_red = 110
        camera.set_feature_value(ECamFeatureId.WhiteBalanceRed, white_balance_red)
        white_balance_red = camera.get_feature_value(ECamFeatureId.WhiteBalanceRed)
        print(f" White Balance Red: {white_balance_red}")

        # # Get White Balance Blue value
        white_balance_blue = camera.get_feature_value(ECamFeatureId.WhiteBalanceBlue)
        print(f" White Balance Blue: {white_balance_blue}")

        # Set format
        # camera.set_feature_value(ECamFeatureId.Format, (ECamFormatColor.ecfcRgb24, ECamFormatSize.ecfsH2880x2048))

        img = camera.get_image()

        print(f'Properties: {camera.get_properties()}')

        # Get White Balance Red value
        white_balance_red = camera.get_feature_value(ECamFeatureId.WhiteBalanceRed)
        print(f" White Balance Red: {white_balance_red}")

    # Display the image
    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    main()
