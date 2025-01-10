import time
import ctypes
from typing import Any

import numpy as np

from . import methods as methods
from . import structures as structs
from . import constants as consts
from . import error_codes as err_codes
from . import commands as cmds


class NikonCamera:
    def __init__(self, camera_index: int = 0, set_defaults: bool = True, trigger_mode: consts.ECamTriggerMode = consts.ECamTriggerMode.Soft) -> None:
        self.camera_index: int = camera_index

        # Get an array of possible devices
        self.device_count, self.device_handles = methods.open_devices()
        if camera_index < 0:
            raise ValueError("Camera index cannot be negative.")
        elif camera_index >= self.device_count:
            raise ConnectionError(f"Camera index unavailable. Must be between 0 and {self.device_count - 1}.")

        # Get the CamDevice object for the specified camera
        self._cam_device = self.device_handles[camera_index]

        # Get camera properties
        self.camera_handle: int = -1  # Camera handle before connection is made
        self.camera_type = consts.ECamDeviceType(self._cam_device.eCamDeviceType)
        self.serial_number: int = int(self._cam_device.uiSerialNo)
        self.camera_name: str = self._cam_device.wszCameraName
        self.driver_version: str = self._cam_device.wszDriverVersion
        self.fpga_version: str = self._cam_device.wszFpgaVersion
        self.fw_version: str = self._cam_device.wszFwVersion
        self.usb_dc_version: str = self._cam_device.wszUsbDcVersion
        self.usb_version: str = self._cam_device.wszUsbVersion

        self.width = 2880
        self.height = 2048

        self.is_connected = False
        self.connect()

        self.update_feature_map()

        self.set_trigger_mode(trigger_mode)

        if set_defaults:
            self.set_defaults()

        # Initialize image structure
        self._stImage = None
        self._initialize_image_structure()
        self._start_FrameTransfer()

    def _initialize_image_structure(self) -> None:
        """Initialize the image structure once for reuse."""
        self._stImage = structs.CAM_Image()
        frame_size = cmds.get_frame_size(self.camera_handle)
        self._stImage.uiDataBufferSize = frame_size.uiFrameSize
        self._stImage.pDataBuffer = (ctypes.c_uint8 * self._stImage.uiDataBufferSize)()

    def _start_FrameTransfer(self) -> None:
        """Start frame transfer."""
        cmds.start_frame_transfer(self.camera_handle)

    def connect(self) -> None:
        """Connect to the camera."""
        self.camera_handle = methods.open_camera(self.camera_index)
        self.is_connected = True

    def set_defaults(self) -> None:
        """Set default camera settings.\n
        Currently sets the format to RGB24 and resolution to 2880x2048."""
        # Set default format after connection
        self.set_feature_value(consts.ECamFeatureId.Format, (consts.ECamFormatColor.ecfcRgb24, consts.ECamFormatSize.ecfsH2880x2048))

    def disconnect(self) -> None:
        """Disconnect from the camera."""
        if not self.is_connected:
            return

        try:
            self.set_trigger_mode(consts.ECamTriggerMode.Off)
            methods.close_camera(self.camera_handle)
            methods.close_devices()
        except Exception as e:
            print(f"Error during camera disconnect: {str(e)}")  # Or use logging.error() if you prefer
        finally:
            self.is_connected = False
            self.camera_handle = -1

    def __repr__(self) -> str:
        return (
            f"Camera Type: {self.camera_type.name}\n"
            f"Camera Name: {self.camera_name}\n"
            f"Serial Number: {self.serial_number}\n"
            f"Firmware Version: {self.fw_version}\n"
            f"USB Version: {self.usb_version}"
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __del__(self):
        if hasattr(self, 'is_connected'):  # Check if initialization completed
            self.disconnect()

    def get_feature_value(self, feature_id: consts.ECamFeatureId, update_map: bool = False):
        """Get the value of a feature.
        Args:
            feature_id (ECamFeatureId (int)): The feature ID.
            update_map (bool): Whether to update the feature map before getting the value.
        Returns:
            The value of the feature.
        """
        # Check if this is available for the camera
        if feature_id not in self.feature_map:
            raise ValueError(f"Feature {feature_id.name} is not available for this camera.")

        if update_map:
            self.update_feature_map()

        # Get the latest feature value
        feature_vector = methods.get_all_features(self.camera_handle)
        for i in range(feature_vector.uiCountUsed):
            if feature_vector.pstFeatureValue[i].uiFeatureId == feature_id:
                return methods.get_feature_value(feature_vector.pstFeatureValue[i])

        raise ValueError(f"Feature {feature_id.name} not found in current feature values")

    def update_feature_map(self) -> None:
        # Get features and values
        self._features_vec: structs.Vector_CAM_FeatureValue = methods.get_all_features(self.camera_handle)
        self._feature_descriptions: list[structs.CAM_FeatureDesc] = methods.get_all_feature_descriptions(self.camera_handle, self._features_vec)

        # Convert features vector to list to be consistent with feature descriptions
        self._features: list[structs.CAM_FeatureValue] = [self._features_vec.pstFeatureValue[i] for i in range(self._features_vec.uiCountUsed)]

        self.feature_map = {
            consts.ECamFeatureId(feature.uiFeatureId): feature  # Store the whole feature object, not just its value
            for feature in self._features
        }

    def set_feature_value(self, feature_id: consts.ECamFeatureId, value) -> None:
        """Set the value of a feature. Some features are only settable to certain ranges,
        and so prefer to use a managed attribute/property to set these."""
        # Check if this is available for the camera
        if feature_id not in self.feature_map:
            raise ValueError(f"Feature {feature_id.name} is not available for this camera.")

        try:
            methods.set_feature_value(self.camera_handle, self.feature_map[feature_id], value)
        except Exception as exc:
            raise exc
        else:  # If no error, update the feature in the map with the new value
            # Get fresh copy of features to ensure we have the updated state
            feature_vector = methods.get_all_features(self.camera_handle)
            for i in range(feature_vector.uiCountUsed):
                if feature_vector.pstFeatureValue[i].uiFeatureId == feature_id:
                    self.feature_map[feature_id] = feature_vector.pstFeatureValue[i]
                    break

    def set_feature_values(self, features: dict[consts.ECamFeatureId, Any]) -> None:
        """Set multiple feature values at once."""
        missing_features = set(features) - set(self.feature_map)
        if missing_features:
            raise ValueError(f"Features {', '.join(f.name for f in missing_features)} are not available for this camera.")

        try:
            methods.set_feature_values(self.camera_handle, {self.feature_map[i]: v for i, v in features.items()})
        except Exception as exc:
            raise exc
        else:
            for i, v in features.items():
                self.feature_map[i] = v

    def set_trigger_mode(self, trigger_mode: consts.ECamTriggerMode) -> None:
        """Set the trigger mode."""
        # Get index of featureValue within features vector for trigger mode
        # methods.set_feature_value(self.camera_handle, self.feature_map[consts.ECamFeatureId.TriggerMode], trigger_mode)
        # Get index of featureValue within features vector for trigger mode
        # TODO Make efficient
        for i in range(self._features_vec.uiCountUsed):
            if self._features_vec.pstFeatureValue[i].uiFeatureId == consts.ECamFeatureId.TriggerMode:
                variant = self._features_vec.pstFeatureValue[i].stVariant
                variant.Value.i32Value = ctypes.c_int32(trigger_mode)

        methods.pDsCamDLL.CAM_SetFeatures(self.camera_handle, ctypes.byref(self._features_vec))

    def set_trigger_on(self) -> None:
        """Set the trigger mode to on."""
        self.set_trigger_mode(consts.ECamTriggerMode.Soft)

    def set_trigger_off(self) -> None:
        """Set the trigger mode to off."""
        # Stop frame transfer before changing trigger mode
        cmds.stop_frame_transfer(self.camera_handle)
        self.set_trigger_mode(consts.ECamTriggerMode.Off)

    def get_image(self) -> np.ndarray:
        """
        Get an image from the camera.
        Returns:
            The image as a numpy array.
        """
        if self._stImage is None:
            raise RuntimeError("Image structure not initialized")

        # Start frame transfer
        # cmds.start_frame_transfer(self.camera_handle)

        # Trigger frame
        methods.send_command(self.camera_handle, consts.CAM_CMD_ONEPUSH_SOFTTRIGGER)

        # Wait for frame ready event
        timeout = 10  # seconds
        start_time_event = time.time()
        while (time.time() - start_time_event) < timeout:
            event_or_none: structs.CAM_Event | None = methods.poll_event(
                self.camera_handle, consts.ECamEventType.ecetImageReceived)
            if (event_or_none is not None) and (event_or_none.eEventType == consts.ECamEventType.ecetImageReceived):
                break

        # Get image using reusable structure
        try:
            methods.get_image(self.camera_handle, self._stImage)
        except Exception as exc:
            raise Exception(f"Error getting image: {str(exc)}") from exc

        # Reshape buffer into an RGB24 image
        # TODO Make dynamic
        height = self.height
        width = self.width
        expected_size = height * width * 3

        img = np.ctypeslib.as_array(self._stImage.pDataBuffer, shape=(self._stImage.uiDataBufferSize,))
        if img.size < expected_size:
            raise ValueError("Image buffer is smaller than expected, cannot reshape.")
        img = img[:expected_size].reshape((height, width, 3))[..., ::-1]  # RGB24 format

        img = img.astype(np.uint8)

        # Wait for trigger ready event
        start_time_event = time.time()
        while time.time() - start_time_event < timeout:
            event_or_none: structs.CAM_Event | None = methods.poll_event(
                self.camera_handle, consts.ECamEventType.ecetTriggerReady)
            if (event_or_none is not None) and (event_or_none.eEventType == consts.ECamEventType.ecetTriggerReady):
                if time.time() - start_time_event > timeout:
                    print("Timeout waiting for trigger ready event")
                break

        # Stop frame transfer - only needed when changing trigger mode to off
        # cmds.stop_frame_transfer(self.camera_handle)

        return img

    def stop_camera(self) -> None:
        """Stop the camera."""
        pass

    def get_properties(self) -> dict:
        """
        Returns the current camera properties\n
        dictkeys:\n
            'gain' : the current gain, 0 means normal gain\n
            'exposure' : the current exposure time in seconds\n
            'gamma' : the gamma of the image, 120 means 1.2 etc..\n
            'white_balance' : the rgb white balance in tuple form e.g. (64,64,64)\n
            'time' : the current time as unix timestamp

        NOTE:
            The exposure time is given in seconds, the gain is given in logical values, the white balance is given in rgb values
            The green value is always returned as 100.
        """
        val_dict = {}
        # get the Gain
        val_dict["gain"] = self.get_feature_value(consts.ECamFeatureId.Gain, update_map=True)

        # ExposureTime = [0]
        val_dict["exposure"] = self.get_feature_value(consts.ECamFeatureId.ExposureTime, update_map=True)

        val_dict["gamma"] = self.get_feature_value(consts.ECamFeatureId.Brightness, update_map=True)

        WBr = self.get_feature_value(consts.ECamFeatureId.WhiteBalanceRed, update_map=True)
        WBb = self.get_feature_value(consts.ECamFeatureId.WhiteBalanceBlue, update_map=True)
        WBg = 100

        val_dict["white_balance"] = (WBr, WBb, WBg)

        val_dict["time"] = time.time()

        return val_dict

    def set_properties(
            self,
            exposure: float = None,
            gain: int = None,
            white_balance: tuple[float, float, float] = None,
            ) -> None:
        """
        Sets camera values\n
        exposure is given in microseconds\n
        gain is given in logical Values, aka 0 is normal gain\n
        white_balance is given as a tuple like (64,64,64) for rbg balance\n

        Args:
            exposure (float): exposure time in microseconds
            gain (int): gain value
            white_balance (tuple): white balance values
            gamma (int): gamma value
        """
        if exposure is not None:
            self.set_feature_value(consts.ECamFeatureId.ExposureTime, exposure)
        if gain is not None:
            self.set_feature_value(consts.ECamFeatureId.Gain, gain)
        if white_balance is not None:
            self.set_feature_value(consts.ECamFeatureId.WhiteBalanceRed, white_balance[0])
            self.set_feature_value(consts.ECamFeatureId.WhiteBalanceBlue, white_balance[2])
