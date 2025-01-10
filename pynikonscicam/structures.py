import ctypes

from . import constants as c


class CAM_Device(ctypes.Structure):
    _fields_ = [
        ("eCamDeviceType", ctypes.c_uint32),
        ("uiSerialNo", ctypes.c_uint32),
        ("wszFwVersion", ctypes.c_wchar * c.CAM_VERSION_MAX),
        ("wszFpgaVersion", ctypes.c_wchar * c.CAM_VERSION_MAX),
        ("wszUsbDcVersion", ctypes.c_wchar * c.CAM_VERSION_MAX),
        ("wszUsbVersion", ctypes.c_wchar * c.CAM_VERSION_MAX),
        ("wszDriverVersion", ctypes.c_wchar * c.CAM_VERSION_MAX),
        ("wszCameraName", ctypes.c_wchar * c.CAM_NAME_MAX),
    ]

    def __init__(self):
        # Initialize all fields to zeros or equivalent
        super().__init__()
        ctypes.memset(ctypes.byref(self), 0, ctypes.sizeof(self))


class CAM_FeatureNameRef(ctypes.Structure):
    _fields_ = [
        ("eId", ctypes.c_uint32),
        ("wszName", ctypes.c_wchar * c.CAM_FEA_COMMENT_MAX),
    ]


class CAM_Area(ctypes.Structure):
    _fields_ = [
        ("uiLeft", ctypes.c_uint32),
        ("uiTop", ctypes.c_uint32),
        ("uiWidth", ctypes.c_uint32),
        ("uiHeight", ctypes.c_uint32),
    ]


class CAM_Position(ctypes.Structure):
    """
    This structure is used to set the feature of position, mainly for setting ROI (Region of Interest) cropping position.
    It is utilized when the eVarType of the CAM_Variant structure is set to evrt_Position.
    """
    _fields_ = [
        ("uiX", ctypes.c_uint32),
        ("uiY", ctypes.c_uint32),
    ]


class CAM_Size(ctypes.Structure):
    """
    This structure is used to set the feature of size, mainly for setting ROI (Region of Interest) cropping size.
    It is utilized when the eVarType of the CAM_Variant structure is set to evrt_Size.
    """
    _fields_ = [
        ("uiWidth", ctypes.c_uint32),
        ("uiHeight", ctypes.c_uint32),
    ]


class CAM_TriggerOption(ctypes.Structure):
    """
    This structure is used to set the feature of Trigger Option, specifically for configuring trigger-related options.
    It is utilized when the eVarType of the CAM_Variant structure is set to evrt_TriggerOption.
    """
    _fields_ = [
        ("uiFrameCount", ctypes.c_uint32),
        ("iDelayTime", ctypes.c_int32),
    ]


class CAM_MultiExposureTime(ctypes.Structure):
    """
    This structure is used to set the feature of multi exposure time, specifically for configuring multiple exposure times.
    It is utilized when the eVarType of the CAM_Variant structure is set to evrt_MultiExposureTime.
    """
    _fields_ = [
        ("uiNum", ctypes.c_uint32),
        ("uiExposureTime", ctypes.c_uint32 * c.CAM_FEA_MULTIEXPOSURETIME_MAX),
    ]


class CAM_Format(ctypes.Structure):
    """
    This structure is used to set the feature of image format, specifically for configuring the color and mode of the image format.
    It is utilized when the eVarType of the CAM_Variant structure is set to evrt_Format.
    """
    _fields_ = [
        ("eColor", ctypes.c_uint32),  # ECamFormatColor as c_uint32
        ("eMode", ctypes.c_uint32),   # EcamFormatMode as c_uint32
    ]


class CAM_Variant(ctypes.Structure):
    """
    This structure is used to set the feature value using a Variant, which allows for multiple types of data to be stored.
    The specific type of data stored is determined by the eVarType field, which references the variant in the union.
    """
    class VariantUnion(ctypes.Union):
        _fields_ = [
            ("i32Value", ctypes.c_int32),
            ("ui32Value", ctypes.c_uint32),
            ("i64Value", ctypes.c_int64),
            ("ui64Value", ctypes.c_uint64),
            ("dValue", ctypes.c_double),
            ("bValue", ctypes.c_bool),
            ("pValue", ctypes.c_void_p),
            ("wszValue", ctypes.c_wchar * c.CAM_FEA_VARIANT_MAX),
            ("stArea", CAM_Area),
            ("stPosition", CAM_Position),
            ("stSize", CAM_Size),
            ("stTriggerOption", CAM_TriggerOption),
            ("stMultiExposureTime", CAM_MultiExposureTime),
            ("stFormat", CAM_Format),
        ]

    _fields_ = [
        ("eVarType", ctypes.c_uint32),  # ECamVariantRunType as c_uint32
        ("Value", VariantUnion),
    ]


class CAM_FeatureValue(ctypes.Structure):
    """
    This structure represents a feature value, containing an identifier for the feature, a variant to hold the feature's value,
    and a transaction size that is not used by the application.
    """
    _fields_ = [
        ("uiFeatureId", ctypes.c_uint32),
        ("stVariant", CAM_Variant),
        ("ucTransSize", ctypes.c_uint8),  # Assuming lx_uchar8 maps to c_uint8
    ]
    def __hash__(self):
        return hash(self.uiFeatureId)


class Vector_CAM_FeatureValue(ctypes.Structure):
    """
    This structure represents an array of feature values, including metadata about the array such as the count of used elements,
    the capacity, and a flag to pause transfer. It holds a pointer to the first element of the array of CAM_FeatureValue structures.
    """
    _fields_ = [
        ("uiCountUsed", ctypes.c_uint32),
        ("uiCapacity", ctypes.c_uint32),
        ("uiPauseTransfer", ctypes.c_uint32),
        ("pstFeatureValue", ctypes.POINTER(CAM_FeatureValue)),
    ]


class CAM_FeatureDescElement(ctypes.Structure):
    """
    This structure is used to set a feature attribute, specifically for when the eFeatureDescType of the CAM_FeatureDesc structure
    is set to edesc_ElementList. It includes a variant to hold the value and a comment.
    """
    _fields_ = [
        ("varValue", CAM_Variant),
        ("wszComment", ctypes.c_wchar * c.CAM_FEA_COMMENT_MAX),
    ]


class CAM_FeatureDescRange(ctypes.Structure):
    """
    This structure is used to set a feature attribute with a range, specifically for when the eFeatureDescType of the CAM_FeatureDesc structure
    is set to edesc_Range. It includes variants to hold the minimum, maximum, resolution, and default values.
    """
    _fields_ = [
        ("stMin", CAM_Variant),
        ("stMax", CAM_Variant),
        ("stRes", CAM_Variant),
        ("stDef", CAM_Variant),
    ]


class CAM_FeatureDescArea(ctypes.Structure):
    """
    This structure is used to set a feature attribute of area, specifically for setting metering areas.
    It is utilized when the eFeatureDescType of the CAM_FeatureDesc structure is set to edesc_Area.
    It includes CAM_Area structures to hold the minimum, maximum, resolution, and default values.
    """
    _fields_ = [
        ("stMin", CAM_Area),
        ("stMax", CAM_Area),
        ("stRes", CAM_Area),
        ("stDef", CAM_Area),
    ]


class CAM_FeatureDescPosition(ctypes.Structure):
    """
    This structure is used to set a feature attribute of position, specifically for setting ROI (Region of Interest) cropping positions.
    It is utilized when the eFeatureDescType of the CAM_FeatureDesc structure is set to edesc_Position.
    It includes CAM_Position structures to hold the minimum, maximum, resolution, and default values.
    """
    _fields_ = [
        ("stMin", CAM_Position),
        ("stMax", CAM_Position),
        ("stRes", CAM_Position),
        ("stDef", CAM_Position),
    ]


class CAM_FeatureDescSize(ctypes.Structure):
    """
    This structure is used to set a feature attribute of size, specifically for setting ROI (Region of Interest) cropping sizes.
    It is utilized when the eFeatureDescType of the CAM_FeatureDesc structure is set to edesc_Size.
    It includes CAM_Size structures to hold the minimum, maximum, resolution, and default values.
    """
    _fields_ = [
        ("stMin", CAM_Size),
        ("stMax", CAM_Size),
        ("stRes", CAM_Size),
        ("stDef", CAM_Size),
    ]


class CAM_FeatureDescTriggerOption(ctypes.Structure):
    """
    This structure is used to set a feature attribute of Trigger Option, specifically for configuring trigger options such as frame count and delay time.
    It is utilized when the eFeatureDescType of the CAM_FeatureDesc structure is set to edesc_TriggerOption.
    It includes CAM_FeatureDescRange structures to define the ranges for frame count and delay time.
    """
    _fields_ = [
        ("stRangeFrameCount", CAM_FeatureDescRange),
        ("stRangeDelayTime", CAM_FeatureDescRange),
    ]


class CAM_FeatureDescFormat(ctypes.Structure):
    """
    This structure is used to set a feature attribute of image format, including details such as image width, height, bits per pixel,
    and a comment. It also includes a list of triggers, and descriptors for area, position, and size attributes.
    It is utilized when the eFeatureDescType of the CAM_FeatureDesc structure is set to edesc_FormatList.
    """
    _fields_ = [
        ("stFormat", CAM_Format),
        ("uiImageWidth", ctypes.c_uint32),
        ("uiImageHeight", ctypes.c_uint32),
        ("uiBitPerPixel", ctypes.c_uint32),
        ("wszComment", ctypes.c_wchar * c.CAM_FEA_COMMENT_MAX),
        ("uiTriggerListCount", ctypes.c_uint32),
        ("stTriggerList", CAM_FeatureDescElement * c.ECamTriggerMode.TriggerMax),
        ("stDescArea", CAM_FeatureDescArea),
        ("stDescPosition", CAM_FeatureDescPosition),
        ("stDescSize", CAM_FeatureDescSize),
    ]


class CAM_FeatureDesc(ctypes.Structure):
    """
    This structure is used to set a feature attribute using a variant approach, where the specific attribute type is determined by eFeatureDescType.
    It can represent a variety of feature descriptions including element lists, ranges, areas, positions, sizes, trigger options, and format lists.
    """
    class _FeatureDescUnion(ctypes.Union):
        _fields_ = [
            ("stElementList", CAM_FeatureDescElement * c.CAM_FEA_DESC_LIST_MAX),
            ("stRange", CAM_FeatureDescRange),
            ("stArea", CAM_FeatureDescArea),
            ("stPosition", CAM_FeatureDescPosition),
            ("stSize", CAM_FeatureDescSize),
            ("stTriggerOption", CAM_FeatureDescTriggerOption),
            ("stFormatList", CAM_FeatureDescFormat * c.CAM_FEA_DESC_LIST_MAX),
        ]

    _fields_ = [
        ("uiFeatureId", ctypes.c_uint32),
        ("uiListCount", ctypes.c_uint32),
        # ("eFeatureDescType", c.ECamFeatureDescType),
        ("eFeatureDescType", ctypes.c_uint32),
        ("FeatureDesc", _FeatureDescUnion),
    ]


class CAM_Image(ctypes.Structure):
    _fields_ = [
        # ("pDataBuffer", ctypes.c_void_p),
        # ("pDataBuffer", ctypes.POINTER(ctypes.c_ubyte)),  #  Cant convert null pointer to ubyte pointer
        ("pDataBuffer", ctypes.POINTER(ctypes.c_uint8)),  #  Cant convert null pointer to ubyte pointer
        ("uiDataBufferSize", ctypes.c_uint32),
        ("uiImageSize", ctypes.c_uint32),
        ("uiEndTime", ctypes.c_uint32),
        ("uiEndTime64", ctypes.c_uint64),
        ("uiFrameCount", ctypes.c_uint64),
        ("uiRefCount", ctypes.c_uint32),
    ]

    # def __init__(self):
    #     super().__init__()
    #     # ctypes.memset(ctypes.byref(self), 0, ctypes.sizeof(self))


class CAM_ImageInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("usFrameNo", ctypes.c_ushort),
        ("usTrggerOptionNo", ctypes.c_ushort),
        ("usMultiExposureTimeNo", ctypes.c_ushort),
        ("ucReserve006", ctypes.c_ubyte * 2),
        ("uiExposureTime", ctypes.c_uint32),
        ("uiFocusLevelR", ctypes.c_uint32),
        ("uiFocusLevelGr", ctypes.c_uint32),
        ("uiFocusLevelGb", ctypes.c_uint32),
        ("uiFocusLevelB", ctypes.c_uint32),
        ("ucReserve028", ctypes.c_ubyte * 36),
        ("ucCameraType", ctypes.c_ubyte),
        ("ucImageMode", ctypes.c_ubyte),
        ("ucImageColor", ctypes.c_ubyte),
        ("ucTriggerMode", ctypes.c_ubyte),
        ("uiSerialNo", ctypes.c_uint32),
        ("uiFwVersion", ctypes.c_uint32),
        ("uiFpgaVersion", ctypes.c_uint32),
        ("usUsbDcVersion", ctypes.c_ushort),
        ("ucReserve082", ctypes.c_ubyte * 2),
        ("usImageWidth", ctypes.c_ushort),
        ("usImageHeight", ctypes.c_ushort),
        ("usRoiLeft", ctypes.c_ushort),
        ("usRoiTop", ctypes.c_ushort),
        ("uiFrameSize", ctypes.c_uint32),
        ("ucExposureMode", ctypes.c_ubyte),
        ("cExposureBias", ctypes.c_char),
        ("ucTone", ctypes.c_ubyte),
        ("ucScene", ctypes.c_ubyte),
        ("ucReserve100", ctypes.c_ubyte * 4),
        ("usGain", ctypes.c_ushort),
        ("sBrightness", ctypes.c_short),
        ("cSharpness", ctypes.c_char),
        ("ucCaptureMode", ctypes.c_ubyte),
        ("ucAeStay", ctypes.c_ubyte),
        ("ucMeteringMode", ctypes.c_ubyte),
        ("usMeteringAreaLeft", ctypes.c_ushort),
        ("usMeteringAreaTop", ctypes.c_ushort),
        ("usMeteringAreaWidth", ctypes.c_ushort),
        ("usMeteringAreaHeight", ctypes.c_ushort),
        ("sHue", ctypes.c_short),
        ("sSaturation", ctypes.c_short),
        ("usWhiteBalanceRed", ctypes.c_ushort),
        ("usWhiteBalanceBlue", ctypes.c_ushort),
        ("usDefect", ctypes.c_ushort),
        ("usWhiteBalanceGreen", ctypes.c_ushort),
        ("ucReserve132", ctypes.c_ubyte * 4),
        ("ucReserve136", ctypes.c_ubyte * 4),
        ("cWhiteBalance", ctypes.c_char),
        ("ucReserve140", ctypes.c_ubyte),
        ("usAutoWhiteBalanceRed", ctypes.c_ushort),
        ("usAutoWhiteBalanceGreen", ctypes.c_ushort),
        ("usAutoWhiteBalanceBlue", ctypes.c_ushort),
        ("usAutoWhiteBalanceX", ctypes.c_ushort),
        ("usAutoWhiteBalanceY", ctypes.c_ushort),
        ("ucReserve152", ctypes.c_char),
        ("cIrcfAdaptor", ctypes.c_char),
        ("usDefect2", ctypes.c_ushort),
        ("ucReserve156", ctypes.c_ubyte * 4),
        ("ucReserve160", ctypes.c_ubyte * 96),
    ]


CAM_IMG_INFO_SIZE = ctypes.sizeof(CAM_ImageInfo)


class CAM_ImageInfoEx(ctypes.Structure):
    class Union(ctypes.Union):
        _fields_ = [
            ("ucInfo", ctypes.c_ubyte * CAM_IMG_INFO_SIZE),
            ("stInfo", CAM_ImageInfo),
        ]

    _anonymous_ = ("_union",)
    _fields_ = [
        ("_union", Union),
    ]

    # def __init__(self):
    #     super().__init__()
    #     ctypes.memset(ctypes.byref(self), 0, ctypes.sizeof(self))

    def CopyInto(self, pInfo):
        ctypes.memcpy(self.ucInfo, pInfo, CAM_IMG_INFO_SIZE)

    def GetInfo(self, stImage):
        self.CopyInto(ctypes.cast(stImage.pDataBuffer, ctypes.POINTER(ctypes.c_ubyte))[stImage.uiImageSize:])
        return ctypes.pointer(self.stInfo)


class CAM_CMD_GetFrameSize(ctypes.Structure):
    _fields_ = [
        ("uiFrameSize", ctypes.c_uint32),       # frame size include ImageInfo
        ("uiFrameInterval", ctypes.c_uint32),   # frame interval
        ("uiRShutterDelay", ctypes.c_uint32),   # RSutter delay (usec)
    ]


class CAM_CMD_StartFrameTransfer(ctypes.Structure):
    _fields_ = [
        ("uiImageBufferNum", ctypes.c_uint32),  # 1 - 128 Driver allocate
    ]


class CAM_CMD_IsTransferStarted(ctypes.Structure):
    _fields_ = [
        ("bStarted", ctypes.c_bool),  # true: Started, false: Stopped
    ]


class CAM_CMD_FrameDropless(ctypes.Structure):
    _fields_ = [
        ("bSet", ctypes.c_bool),   # true: Set, false: Get
        ("bOnOff", ctypes.c_bool), # true: ON, false: OFF
    ]


class CAM_CMD_Grouping(ctypes.Structure):
    _fields_ = [
        ("bSet", ctypes.c_bool),  # true: Set, false: Get
        ("ucGroup", ctypes.c_ubyte * c.CAM_DEVICE_MAX),  # Array of group settings
    ]


class CAM_CMD_GetSdkVersion(ctypes.Structure):
    _fields_ = [
        ("wszSdkVersion", ctypes.c_wchar * c.CAM_VERSION_MAX),  # SDK Version string
    ]


class CAM_CMD_ControlCis(ctypes.Structure):
    _fields_ = [
        ("bSet", ctypes.c_bool),    # true: Set, false: Get
        ("ucState", ctypes.c_ubyte),  # 0: Down, 1: Run
    ]


class CAM_CMD_CheckFwVersion(ctypes.Structure):
    _fields_ = [
        ("bValid", ctypes.c_bool),  # true: Valid, false: Invalid
        ("wszInvalidReason", ctypes.c_wchar * c.CAM_CMD_STRING_MAX),  # Reason for invalidation
    ]


class CAM_CMD_FovSize(ctypes.Structure):
    """
    If you set true to bFreeRoi, you can define ROI and Metering areas in 1 pixel unit regardless of camera restrictions.
    However, please note that SDK might adjust the Metering area automatically to set the minimum area beyond the camera restrictions.
    """
    _fields_ = [
        ("bFreeRoi", ctypes.c_bool),  # Is free setting
        ("uiFovMode", ctypes.c_uint32),  # FOV mode (0: Cancel, 1: Full, 2: HD, 3: 25Phi, 4: 22Phi, 5: 16Phi)
        ("stFovSize", CAM_Size),  # FovSize-Value
        ("stDeskSize", CAM_FeatureDescSize),  # RoiSize-Desk
        ("stDeskPosition", CAM_FeatureDescPosition),  # RoiPosition-Desk
        ("stDeskArea", CAM_FeatureDescArea),  # RoiMeteringArea-Desk
    ]


class CAM_CMD_FovRoi(ctypes.Structure):
    _fields_ = [
        ("stSize", CAM_Size),       # RoiSize-Value
        ("stPosition", CAM_Position),  # RoiPosition-Value
        ("stArea", CAM_Area),       # RoiMeteringArea-Value
    ]


class CAM_EventFeatureChanged(ctypes.Structure):
    _fields_ = [
        ("uiTick", ctypes.c_uint32),      # Tick count
        ("uiTick64", ctypes.c_uint64),    # 64-bit tick count
        ("uiFeatureId", ctypes.c_uint32), # Feature ID
        ("stVariant", CAM_Variant),       # Feature value
    ]


class CAM_EventSignal(ctypes.Structure):
    _fields_ = [
        ("uiTick", ctypes.c_uint32),      # Tick count
        ("uiTick64", ctypes.c_uint64),    # 64-bit tick count
        # ("eEventType", c.ECamEventType),    # Event type
        ("eEventType", ctypes.c_int),    # Event type
    ]


class CAM_EventBusReset(ctypes.Structure):
    _fields_ = [
        ("uiTick", ctypes.c_uint32),                # Tick count
        ("uiTick64", ctypes.c_uint64),              # 64-bit tick count
        # ("eBusResetCode", c.ECamEventBusResetCode),   # Bus reset code
        ("eBusResetCode", ctypes.c_int),   # Bus reset code
        ("bImageCleared", ctypes.c_bool),           # Image cleared flag
    ]


class CAM_EventImageReceived(ctypes.Structure):
    _fields_ = [("uiTick", ctypes.c_uint32),
                ("uiTick64", ctypes.c_uint64),
                ("uiFrameNo", ctypes.c_uint32),
                ("uiRemained", ctypes.c_uint32)]


class CAM_EventTransError(ctypes.Structure):
    _fields_ = [("uiTick", ctypes.c_uint32),
                ("uiTick64", ctypes.c_uint64),
                ("uiUsbErrorCode", ctypes.c_uint32),
                ("uiDriverErrorCode", ctypes.c_uint32),
                ("uiReceivedSize", ctypes.c_uint32),
                ("uiSettingSize", ctypes.c_uint32)]


class CAM_Event(ctypes.Structure):
    class _EventUnion(ctypes.Union):
        _fields_ = [
            ("stImageReceived", CAM_EventImageReceived),
            ("stFeatureChanged", CAM_EventFeatureChanged),
            ("stSignal", CAM_EventSignal),
            ("stTransError", CAM_EventTransError),
            ("stBusReset", CAM_EventBusReset),
        ]

    _anonymous_ = ("_eventUnion",)
    _fields_ = [
        # ("eEventType", c.ECamEventType),
        ("eEventType", ctypes.c_uint32),
        ("_eventUnion", _EventUnion),
    ]


class CAM_NoticeTransError(ctypes.Structure):
    _fields_ = [
        ("uiTick", ctypes.c_uint32),            # Tick count
        ("uiTick64", ctypes.c_uint64),          # 64-bit tick count
        ("uiRequestCode", ctypes.c_uint32),     # Request code
        ("uiCameraErrorCode", ctypes.c_uint32), # Camera error code
        ("uiUsbErrorCode", ctypes.c_uint32),    # USB error code
        ("uiDriverErrorCode", ctypes.c_uint32), # Driver error code
    ]


class CAM_NoticeGroup(ctypes.Structure):
    _fields_ = [
        ("uiTick", ctypes.c_uint32),                # Tick count
        ("uiTick64", ctypes.c_uint64),              # 64-bit tick count
        # ("eCode", c.ECamNoticeGroupCode),             # Group notice code
        ("eCode", ctypes.c_int),             # Group notice code
        ("iDetail", ctypes.c_int32),                # Detail information
        ("wszComment", ctypes.c_wchar * c.CAM_TEXT_MAX),  # Comment
    ]


class CAM_NoticeInfo(ctypes.Structure):
    _fields_ = [
        ("uiTick", ctypes.c_uint32),                # Tick count
        ("uiTick64", ctypes.c_uint64),              # 64-bit tick count
        # ("eCode", c.ECamNoticeInfoCode),              # Information notice code
        ("eCode", ctypes.c_int),              # Information notice code
        ("iValue", ctypes.c_int32),                 # Integer value
        ("dValue", ctypes.c_double),                # Double value
        ("bValue", ctypes.c_bool),                  # Boolean value
        ("wszText", ctypes.c_wchar * c.CAM_TEXT_MAX), # Text
    ]


class CAM_Notice(ctypes.Structure):
    class _NoticeUnion(ctypes.Union):
        _fields_ = [
            ("stTransError", CAM_NoticeTransError),
            ("stGroup", CAM_NoticeGroup),
            ("stInfo", CAM_NoticeInfo),
        ]

    _anonymous_ = ("_noticeUnion",)
    _fields_ = [
        # ("eNoticeType", c.ECamNoticeType),
        ("eNoticeType", ctypes.c_int),
        ("_noticeUnion", _NoticeUnion),
    ]
