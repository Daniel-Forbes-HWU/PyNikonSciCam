import os
import ctypes
from typing import Any

from . import structures as s
from . import constants as c
from .error_codes import ErrorCodes

dllpath = os.path.join(os.path.dirname(__file__), "DsCam.dll")
pDsCamDLL = ctypes.WinDLL(dllpath)

# Define function prototypes according to the provided SDK API documentation

# CAM_OpenDevices
pDsCamDLL.CAM_OpenDevices.argtypes = [
    ctypes.POINTER(ctypes.c_uint32),  # OUT lx_uint32& uiDeviceCount
    ctypes.POINTER(ctypes.POINTER(s.CAM_Device))  # OUT CAM_Device** ppstCamDevice
]
pDsCamDLL.CAM_OpenDevices.restype = ErrorCodes


def open_devices():
    """Open all available devices and return the device count and device list.
    Returns:
        int: Number of devices
        ctypes.POINTER(s.CAM_Device): List of devices
    """
    uiDeviceCount = ctypes.c_uint32()
    ppstCamDevice = ctypes.POINTER(s.CAM_Device)()
    result = pDsCamDLL.CAM_OpenDevices(ctypes.byref(uiDeviceCount), ctypes.byref(ppstCamDevice))

    if result != ErrorCodes.OK:
        raise Exception(f"Failed to open devices. Error code: {ErrorCodes(result)}, device count: {uiDeviceCount.value}")
    return uiDeviceCount.value, ppstCamDevice


# CAM_CloseDevices
pDsCamDLL.CAM_CloseDevices.argtypes = []
pDsCamDLL.CAM_CloseDevices.restype = ErrorCodes


def close_devices() -> None:
    """Release connected devices.
    NOTE Only call once all connected cameras have disconnected."""
    result = pDsCamDLL.CAM_CloseDevices()
    if result != ErrorCodes.OK:
        raise Exception(f"Failed to close devices. Error code: {ErrorCodes(result)}")


# CAM_Open
pDsCamDLL.CAM_Open.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiDeviceIndex
    ctypes.POINTER(ctypes.c_uint32),  # OUT lx_uint32& uiCameraHandle
    ctypes.c_uint32,  # IN const lx_uint32 uiErrMsgMaxSize
    ctypes.POINTER(ctypes.c_wchar)  # OUT lx_wchar* pwszErrMsg
]
pDsCamDLL.CAM_Open.restype = ErrorCodes


def open_camera(device_index: int) -> int:
    """Open a camera with the specified serial number.
    Args:
        uiSerialNo (int): Serial number of the camera
    Returns:
        int: Camera handle
    """
    uiCameraHandle = ctypes.c_uint32()
    uiErrMsgMaxSize = c.CAM_ERRMSG_MAX
    pwszErrMsg = ctypes.create_unicode_buffer(uiErrMsgMaxSize)
    result = pDsCamDLL.CAM_Open(device_index, ctypes.byref(uiCameraHandle), uiErrMsgMaxSize, pwszErrMsg)

    if result != ErrorCodes.OK:
        raise Exception(f"Failed to open camera. Error code: {ErrorCodes(result)}, error message: {pwszErrMsg.value}")
    return uiCameraHandle.value


# CAM_Close
pDsCamDLL.CAM_Close.argtypes = [
    ctypes.c_uint32  # IN const lx_uint32 uiCameraHandle
]
pDsCamDLL.CAM_Close.restype = ErrorCodes


def close_camera(camera_handle: int) -> None:
    """Close the camera with the specified handle.
    Args:
        uiCameraHandle (int): Camera handle
    """
    result = pDsCamDLL.CAM_Close(camera_handle)
    if result != ErrorCodes.OK:
        raise Exception(f"Failed to close camera. Error code: {ErrorCodes(result)}")


# CAM_GetAllFeatures
pDsCamDLL.CAM_GetAllFeatures.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
    ctypes.POINTER(s.Vector_CAM_FeatureValue)  # OUT Vector_CAM_FeatureValue& vectFeatureValue
]
pDsCamDLL.CAM_GetAllFeatures.restype = ErrorCodes


def get_all_features(camera_handle: int) -> s.Vector_CAM_FeatureValue:
    """Get all features of the camera with the specified handle.
    Args:
        uiCameraHandle (int): Camera handle
    Returns:
        Vector_CAM_FeatureValue: List of features
    """
    vectFeatureValue = s.Vector_CAM_FeatureValue()

    # Configure the feature value capacity
    vectFeatureValue.uiCapacity = c.CAM_FEA_CAPACITY
    vectFeatureValue.pstFeatureValue = (s.CAM_FeatureValue * c.CAM_FEA_CAPACITY)()

    result = pDsCamDLL.CAM_GetAllFeatures(camera_handle, ctypes.byref(vectFeatureValue))

    if result != ErrorCodes.OK:
        raise Exception(f"Failed to get all features. Error code: {ErrorCodes(result)}")
    return vectFeatureValue

# CAM_GetFeatures
pDsCamDLL.CAM_GetFeatures.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
    ctypes.POINTER(s.Vector_CAM_FeatureValue)  # INOUT Vector_CAM_FeatureValue& vectFeatureValue
]
pDsCamDLL.CAM_GetFeatures.restype = ErrorCodes

# CAM_SetFeatures
pDsCamDLL.CAM_SetFeatures.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
    ctypes.POINTER(s.Vector_CAM_FeatureValue)  # INOUT Vector_CAM_FeatureValue& vectFeatureValue
]
pDsCamDLL.CAM_SetFeatures.restype = ErrorCodes


def set_feature_value(camera_handle: int, feature: s.CAM_FeatureValue, value) -> None:
    # Ensure it is the enum
    feature_id: int = feature.uiFeatureId

    # Create vector of FeatureValue
    features = s.Vector_CAM_FeatureValue()
    # features.uiCapacity = c.CAM_FEA_CAPACITY  # Likely excessive
    features.uiCapacity = 1
    features.uiCountUsed = 1
    features.pstFeatureValue = ctypes.pointer(feature)

    match feature_id:
        case c.ECamFeatureId.Format:
            value: tuple[c.ECamFormatColor, c.ECamFormatSize] = value
            setattr(feature.stVariant.Value, c.VarTypeAttrMap[feature.stVariant.eVarType], value)
        case _:
            setattr(feature.stVariant.Value, c.VarTypeAttrMap[feature.stVariant.eVarType], int(value))

    # setattr(feature.stVariant.Value, c.VarTypeAttrMap[feature.stVariant.eVarType], value)
    # setattr(feature.stVariant.Value, c.VarTypeAttrMap[feature.stVariant.eVarType], int(value))

    result = pDsCamDLL.CAM_SetFeatures(camera_handle, ctypes.byref(features))

    # features is updated above, TODO Add check for updated value?
    if result != ErrorCodes.OK:
        raise Exception(f"Failed to set feature {feature_id}. Error code: {ErrorCodes(result).name}")


def set_feature_values(camera_handle: int, features: dict[s.CAM_FeatureValue, Any]) -> None:
    """Set multiple features of the camera with the specified handle.
    Args:
        uiCameraHandle (int): Camera handle
        features (dict[CAM_FeatureValue, Any]): Dictionary of features and their values

    Raises:
        Exception: If setting the features fails for any reason

    Example:
        set_feature_values(camera_handle, features={feature1: value1, feature2: value2})
    """
    # Create vector of FeatureValue
    features_vector = s.Vector_CAM_FeatureValue()
    features_vector.uiCapacity = len(features)
    features_vector.uiCountUsed = len(features)
    features_vector.pstFeatureValue = (s.CAM_FeatureValue * len(features))()

    for i, (feature, value) in enumerate(features.items()):
        # feature_id = feature.uiFeatureId
        features_vector.pstFeatureValue[i] = feature
        setattr(feature.stVariant.Value, c.VarTypeAttrMap[feature.stVariant.eVarType], int(value))

    result = pDsCamDLL.CAM_SetFeatures(camera_handle, ctypes.byref(features_vector))

    # features is updated above, TODO Add check for updated value?
    if result != ErrorCodes.OK:
        failed_features = [feature.uiFeatureId for feature in features.items()]
        raise Exception(f"Failed to set features {failed_features}. Error code: {ErrorCodes(result).name}")


def set_features(camera_handle: int, features: s.Vector_CAM_FeatureValue) -> None:
    """Set multiple features of the camera with the specified handle.
    Args:
        uiCameraHandle (int): Camera handle
        vectFeatureValue (Vector_CAM_FeatureValue): Array of features
    """
    result = pDsCamDLL.CAM_SetFeatures(camera_handle, ctypes.byref(features))

    if result != ErrorCodes.OK:
        raise Exception(f"Failed to set features. Error code: {ErrorCodes(result)}")


# CAM_GetFeatureDesc
pDsCamDLL.CAM_GetFeatureDesc.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
    ctypes.c_uint32,  # IN lx_uint32 uiFeatureId
    ctypes.POINTER(s.CAM_FeatureDesc)  # OUT CAM_FeatureDesc& stFeatureDesc
]
pDsCamDLL.CAM_GetFeatureDesc.restype = ErrorCodes


def get_all_feature_descriptions(camera_handle: int, features: s.Vector_CAM_FeatureValue) -> list[s.CAM_FeatureDesc]:
    """Get the description of all features of the camera with the specified handle.
    Args:
        uiCameraHandle (int): Camera handle
        vectFeatureValue (Vector_CAM_FeatureValue): List of features
    Returns:
        list[CAM_FeatureDesc]: List of feature descriptions

    NOTE: Unable to determine what each feature actually is...
    """
    # Create array of feature descriptions
    feature_descs = (s.CAM_FeatureDesc * features.uiCapacity)()

    # Get description of each feature
    feature_descriptions = []
    for i in range(features.uiCountUsed):
        feature = features.pstFeatureValue[i]
        stFeatureDesc = feature_descs[i]
        result = pDsCamDLL.CAM_GetFeatureDesc(camera_handle, int(feature.uiFeatureId), ctypes.byref(stFeatureDesc))

        if result != ErrorCodes.OK:
            raise Exception(f"Failed to get feature description. Error code: {ErrorCodes(result)}")
        feature_descriptions.append(stFeatureDesc)

    return feature_descriptions


def get_feature_desc(camera_handle: int, feature_id: int) -> s.CAM_FeatureDesc:
    """Get the description of the feature with the specified ID.
    Args:
        uiCameraHandle (int): Camera handle
        uiFeatureId (int): Feature ID
    Returns:
        CAM_FeatureDesc: Feature description
    """
    stFeatureDesc = s.CAM_FeatureDesc()
    result = pDsCamDLL.CAM_GetFeatureDesc(camera_handle, int(feature_id), ctypes.byref(stFeatureDesc))

    if result != ErrorCodes.OK:
        raise Exception(f"Failed to get feature description. Error code: {ErrorCodes(result)}")
    return stFeatureDesc


def get_feature_value(feature: s.CAM_FeatureValue):
    """
    Get the value of the specified feature.
    Args:
        feature (CAM_FeatureValue): Feature value

    Returns:
        (int | float | bool | ctypes.Pointer | str
         | AreaFeature | PositionFeature | TriggerOptionFeature
         | MultiExposureTimeFeature | FormatFeature | SizeFeature
        ): The value of the feature converted to a Python object.
    """
    variant_value: s.CAM_Variant = feature.stVariant.Value
    variant_type: c.ECamVariantRunType = feature.stVariant.eVarType
    match variant_type:
        # TODO - Add guard and more cases to match e.g. exposure mode, returning the enum instead
        case (c.ECamVariantRunType.evrt_int32
              | c.ECamVariantRunType.evrt_uint32
              | c.ECamVariantRunType.evrt_int64
              | c.ECamVariantRunType.evrt_uint64):
            return int(variant_value.i64Value)

        case c.ECamVariantRunType.evrt_double:
            return float(variant_value.dValue)

        case c.ECamVariantRunType.evrt_bool:
            return bool(variant_value.bValue)

        case c.ECamVariantRunType.evrt_voidptr:
            # return None
            return variant_value.pValue

        case c.ECamVariantRunType.evrt_wstr:
            return str(variant_value.wszValue)

        case c.ECamVariantRunType.evrt_Area:
            return c.AreaFeature(
                height=int(variant_value.stArea.uiHeight),
                left=int(variant_value.stArea.uiLeft),
                top=int(variant_value.stArea.uiTop),
                width=int(variant_value.stArea.uiWidth)
            )

        case c.ECamVariantRunType.evrt_Position:
            return c.PositionFeature(
                x=int(variant_value.stPosition.uiX),
                y=int(variant_value.stPosition.uiY)
            )

        case c.ECamVariantRunType.evrt_TriggerOption:
            return c.TriggerOptionFeature(
                delay_time=int(variant_value.stTriggerOption.iDelayTime),
                frame_count=int(variant_value.stTriggerOption.uiFrameCount)
            )

        case c.ECamVariantRunType.evrt_MultiExposureTime:
            exposure_time_length = variant_value.stMultiExposureTime.uiExposureTime._length_
            return c.MultiExposureTimeFeature(
                num_exposures=int(variant_value.stMultiExposureTime.uiNum),
                exposure_times=[int(variant_value.stMultiExposureTime.uiExposureTime[i]) for i in range(exposure_time_length)]
            )

        case c.ECamVariantRunType.evrt_Format:
            return c.FormatFeature(
                colour=c.ECamFormatColor(variant_value.stFormat.eColor),
                mode=c.ECamFormatSize(variant_value.stFormat.eMode)
            )

        case c.ECamVariantRunType.evrt_Size:
            return c.SizeFeature(
                height=int(variant_value.stSize.uiHeight),
                width=int(variant_value.stSize.uiWidth)
            )

        case c.ECamVariantRunType.evrt_unknown:
            raise ValueError("feature value is specified as unknown.")

        case _:
            raise RuntimeError("Unknown feature value type.")


# CAM_GetImage
pDsCamDLL.CAM_GetImage.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
    ctypes.c_bool,  # IN bool bNewestRequired
    ctypes.POINTER(s.CAM_Image),  # INOUT CAM_Image& stImage
    ctypes.POINTER(ctypes.c_uint32)  # OUT lx_uint32& uiRemained
]
pDsCamDLL.CAM_GetImage.restype = ErrorCodes


def get_image(camera_handle: int, stImage: s.CAM_Image, b_newest_required: bool = True):
    uiRemained = ctypes.c_uint32(0)
    result = pDsCamDLL.CAM_GetImage(camera_handle, b_newest_required, ctypes.byref(stImage), ctypes.byref(uiRemained))

    if result != ErrorCodes.OK:
        raise Exception(f"Failed to get image. Error code: {ErrorCodes(result).name}")


# CAM_Command
pDsCamDLL.CAM_Command.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
    ctypes.c_wchar_p,  # IN const lx_wchar* pwszCommand
    ctypes.c_void_p  # INOUT void* pData
]
pDsCamDLL.CAM_Command.restype = ErrorCodes


def send_command(camera_handle: int, command: str, data = None) -> None:
    """Send a command to the camera.
    Args:
        uiCameraHandle (int): Camera handle
        pwszCommand (str): Command to send
        pData (ctypes.c_void_p): Data to send, varies based on commands, see SDK documentation.
    """
    result = pDsCamDLL.CAM_Command(camera_handle, command, data)

    if result != ErrorCodes.OK:
        raise Exception(f"Failed to send command. Error code: {ErrorCodes(result)}")


# CAM_EventPolling
pDsCamDLL.CAM_EventPolling.argtypes = [
    ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
    ctypes.c_void_p,  # IN const HANDLE hStopEvent
    ctypes.c_int,  # IN ECamEventType eEventType
    ctypes.POINTER(s.CAM_Event)  # OUT CAM_Event* pstEvent
]
pDsCamDLL.CAM_EventPolling.restype = ErrorCodes


def poll_event(camera_handle: int, e_event_type: c.ECamEventType) -> s.CAM_Event | None:
    """Poll for an event.
    NOTE Only non-blocking mode is implemented for now.
    Args:
        uiCameraHandle (int): Camera handle
        eEventType (ECamEventType): Event type
    Returns:
        CAM_Event | None: Event if event is available, else None
    """
    pstEvent = s.CAM_Event()
    result = pDsCamDLL.CAM_EventPolling(camera_handle, None, e_event_type, ctypes.byref(pstEvent))

    if result == ErrorCodes.ERR_ACCESSDENIED:  # No event available
        return None
    elif result != ErrorCodes.OK:
        raise Exception(f"Failed to poll event. Error code: {ErrorCodes(result).name}")

    return pstEvent

# # CAM_SetNoticeCallback
# pDsCamDLL.CAM_SetNoticeCallback.argtypes = [
#     ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
#     s.FCAM_NoticeCallback,  # IN FCAM_NoticeCallback fCAM_NoticeCallback
#     ctypes.c_void_p  # IN void* pTransData
# ]
# pDsCamDLL.CAM_SetNoticeCallback.restype = ErrorCodes

# # CAM_SetEventCallback
# pDsCamDLL.CAM_SetEventCallback.argtypes = [
#     ctypes.c_uint32,  # IN const lx_uint32 uiCameraHandle
#     s.FCAM_EventCallback,  # IN FCAM_EventCallback fCAM_EventCallback
#     ctypes.c_void_p  # IN void* pTransData
# ]
# pDsCamDLL.CAM_SetEventCallback.restype = ErrorCodes
