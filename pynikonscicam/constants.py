from enum import IntEnum
from typing import NamedTuple

# Constants for device management, error messages, versions, and more
CAM_DEVICE_MAX = 32  # Maximum number of devices
CAM_ERRMSG_MAX = 256  # Maximum error message length
CAM_VERSION_MAX = 16  # Maximum version length
CAM_TEXT_MAX = 256  # Maximum text length
CAM_NAME_MAX = 32  # Maximum name length
CAM_FEA_CAPACITY = 64  # Maximum number of features
CAM_FEA_VARIANT_MAX = 256  # Maximum variant length
CAM_FEA_COMMENT_MAX = 64  # Maximum comment length
CAM_FEA_DESC_LIST_MAX = 256  # Maximum number of feature attribute list
CAM_FEA_MULTIEXPOSURETIME_MAX = 15  # Maximum number of multi-exposure time
CAM_FEA_FRAME_SIZE_MAX = 143460000  # Maximum frame size

# Command strings for various operations
CAM_CMD_ONEPUSH_AE = "CAM_CMD_ONEPUSH_AE"  # Command string for one-push AE
CAM_CMD_ONEPUSH_WHITEBALANCE = "CAM_CMD_ONEPUSH_WHITEBALANCE"  # Command string for one-push white balance
CAM_CMD_ONEPUSH_SOFTTRIGGER = "CAM_CMD_ONEPUSH_SOFTTRIGGER"  # Command string for one-push soft trigger
CAM_CMD_ONEPUSH_TRIGGERCANCEL = "CAM_CMD_ONEPUSH_TRIGGERCANCEL"  # Command string for one-push trigger cancel
CAM_CMD_GET_FRAMESIZE = "CAM_CMD_GET_FRAMESIZE"  # Command string for getting frame size
CAM_CMD_START_FRAMETRANSFER = "CAM_CMD_START_FRAMETRANSFER"  # Command string for starting frame transfer
CAM_CMD_STOP_FRAMETRANSFER = "CAM_CMD_STOP_FRAMETRANSFER"  # Command string for stopping frame transfer
CAM_CMD_IS_TRANSFER_STARTED = "CAM_CMD_IS_TRANSFER_STARTED"  # Command string for checking if transfer has started
CAM_CMD_FOV_SIZE = "CAM_CMD_FOV_SIZE"  # Command string for field of view size
CAM_CMD_FOV_ROI = "CAM_CMD_FOV_ROI"  # Command string for field of view region of interest
CAM_CMD_FRAME_DROPLESS = "CAM_CMD_FRAME_DROPLESS"  # Command string for frame dropless
CAM_CMD_GROUPING = "CAM_CMD_GROUPING"  # Command string for grouping
CAM_CMD_GET_SDKVERSION = "CAM_CMD_GET_SDKVERSION"  # Command string for getting SDK version
CAM_CMD_CONTROL_CIS = "CAM_CMD_CONTROL_CIS"  # Command string for controlling CIS
CAM_CMD_CHECK_FW_VERSION = "CAM_CMD_CHECK_FW_VERSION"  # Command string for checking firmware version

CAM_CMD_STRING_MAX = 128  # Maximum command string length


class ECamDeviceType(IntEnum):
    ecdtUnknown = 0
    Ri2 = 1
    Ri2_Simulator = 2
    Qi2 = 3
    Qi2_Simulator = 4
    Fi3 = 5
    Fi3_Simulator = 6
    DS10 = 7
    DS10_Simulator = 8


class ECamExposureMode(IntEnum):
    ContinuousAE = 0
    OnePushAE = 1
    Manual = 2
    MultiExposureTime = 3


class ECamMeteringMode(IntEnum):
    Average = 1
    Peak = 2


class ECamTone(IntEnum):
    Unknown = 0
    WideDinamicRange = 1
    ContrastWeak = 2
    ContrastNomal = 3
    ContrastStrong = 4
    Linear = 5
    MetalOrganization = 6
    ContrastEmphasis = 7


class ECamWhiteBalance(IntEnum):
    wbManual = 0
    wbOnePush = 1
    wbAuto = 2


class ECamPresetsId(IntEnum):
    ecpiDefault = 0
    ecpiIndustry_WaferIc = 16
    ecpiIndustry_Metal = 17
    ecpiIndustry_CircuitBoard = 18
    ecpiIndustry_Fpd = 19
    ecpiBio_BrightField = 32
    ecpiBio_He = 33
    ecpiBio_Ela = 34
    ecpiBioLed_BrightField = 48
    ecpiBioHighLed_BrightField = 49
    ecpiBioHighLed_He = 50
    ecpiBioHighLed_Ela = 51
    ecpiOther_Asbestos = 64
    ecpiOther_Linear = 80


class ECamSignalOutput(IntEnum):
    ecsoOff = 0
    ecsoOutput = 1
    ecsoLast = 2


class ECamFormatColor(IntEnum):
    ecfcUnknown = 0
    ecfcRgb24 = 1
    ecfcYuv444 = 2
    ecfcMono16 = 3
    ecfcRgb48 = 4
    ecfcY16 = 5
    ecfcRaw16 = 6


class ECamFormatSize(IntEnum):
    ecfsUnknown = 0
    ecfs4908x3264 = 1
    ecfs2454x1632 = 2
    ecfs1636x1088 = 3
    ecfs818x544 = 4
    ecfs1608x1608 = 5
    ecfs804x804 = 6
    ecfs536x536 = 7
    ecfs22p2136x2136 = 8
    ecfs22p712x712 = 9
    ecfs25p2424x2424 = 10
    ecfs25p808x808 = 11
    ecfs17p1608x1608 = 12
    ecfs17p536x536 = 13
    ecfsH2880x2048 = 1
    ecfsH1440x1024Roi = 2
    ecfsH1440x1024 = 3
    ecfsH3096x2088 = 4
    ecfsH1548x1044 = 5
    ecfmA6000x3984 = 1
    ecfmA3000x1992 = 2
    ecfmA2000x1328 = 3
    ecfmA6104x4086 = 4
    ecfmA6104x2046 = 5
    ecfmA3052x2046 = 6
    ecfmA2035x1360 = 7


class ECamFeatureId(IntEnum):
    """Maps names to FeatureValue IDs."""
    Unknown = 0
    ExposureMode = 1
    ExposureBias = 2
    ExposureTime = 3
    Gain = 4
    MeteringMode = 5
    MeteringArea = 6
    ExposureTimeLimit = 7
    GainLimit = 8
    CaptureMode = 9
    Brightness = 13
    Sharpness = 14
    Hue = 15
    Saturation = 16
    Tone = 17
    WhiteBalanceRed = 18
    WhiteBalanceBlue = 19
    WhiteBalanceGreen = 20
    WhiteBalance = 25
    Presets = 26
    MeteringAim = 27
    TriggerOption = 33
    OnePushSoftTrigger = 34
    MultiExposureTime = 35
    SignalExposureEnd = 36
    SignalTriggerReady = 37
    SignalDeviceCapture = 38
    ExposureOutput = 39
    OnePushTriggerCancel = 40
    CisPower = 41
    IrcfAdaptor = 42
    Format = 80
    RoiPosition = 81
    TriggerMode = 82
    RoiSize = 83


class AreaFeature(NamedTuple):
    height: int
    left: int
    top: int
    width: int


class PositionFeature(NamedTuple):
    x: int
    y: int


class TriggerOptionFeature(NamedTuple):
    delay_time: int
    frame_count: int


class MultiExposureTimeFeature(NamedTuple):
    num_exposures: int
    exposure_times: list[int]


class FormatFeature(NamedTuple):
    colour: ECamFormatColor
    mode: ECamFormatSize


class SizeFeature(NamedTuple):
    height: int
    width: int


class ECamTriggerMode(IntEnum):
    Off = 0
    Hard = 1
    Soft = 2
    # ectmBoth = 3  # Application can't use
    TriggerMax = 3,


class ECamVariantRunType(IntEnum):
    evrt_unknown = 0
    evrt_int32 = 1
    evrt_uint32 = 2
    evrt_int64 = 3
    evrt_uint64 = 4
    evrt_double = 5
    evrt_bool = 6
    evrt_voidptr = 7
    evrt_wstr = 8
    evrt_Area = 9
    evrt_Position = 10
    evrt_TriggerOption = 11
    evrt_MultiExposureTime = 12
    evrt_Format = 13
    evrt_Size = 14


# Map of attribute names for the VariantRunType Union
VarTypeAttrMap: dict[int, str] = {
    # ECamVariantRunType.evrt_unknown: "",  # No attr for unknown types
    ECamVariantRunType.evrt_int32: "i32Value",
    ECamVariantRunType.evrt_uint32: "ui32Value",
    ECamVariantRunType.evrt_int64: "i64Value",
    ECamVariantRunType.evrt_uint64: "ui64Value",
    ECamVariantRunType.evrt_double: "dValue",
    ECamVariantRunType.evrt_bool: "bValue",
    ECamVariantRunType.evrt_voidptr: "pValue",
    ECamVariantRunType.evrt_wstr: "wszValue",
    ECamVariantRunType.evrt_Area: "stArea",
    ECamVariantRunType.evrt_Position: "stPosition",
    ECamVariantRunType.evrt_TriggerOption: "stTriggerOption",
    ECamVariantRunType.evrt_MultiExposureTime: "stMultiExposureTime",
    ECamVariantRunType.evrt_Format: "stFormat",
    ECamVariantRunType.evrt_Size: "stSize",
}


# Map of Runtypes for each Feature ID
FeatureIDVarTypeMap: dict[int, int] = {
    ECamFeatureId.ExposureMode: ECamVariantRunType.evrt_int32,
    ECamFeatureId.ExposureBias: ECamVariantRunType.evrt_double,
    ECamFeatureId.ExposureTime: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Gain: ECamVariantRunType.evrt_int32,
    ECamFeatureId.MeteringMode: ECamVariantRunType.evrt_int32,
    ECamFeatureId.MeteringArea: ECamVariantRunType.evrt_Area,
    ECamFeatureId.ExposureTimeLimit: ECamVariantRunType.evrt_int32,
    ECamFeatureId.GainLimit: ECamVariantRunType.evrt_int32,
    ECamFeatureId.CaptureMode: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Brightness: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Sharpness: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Hue: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Saturation: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Tone: ECamVariantRunType.evrt_int32,
    ECamFeatureId.WhiteBalanceRed: ECamVariantRunType.evrt_int32,
    ECamFeatureId.WhiteBalanceBlue: ECamVariantRunType.evrt_int32,
    ECamFeatureId.WhiteBalanceGreen: ECamVariantRunType.evrt_int32,
    ECamFeatureId.WhiteBalance: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Presets: ECamVariantRunType.evrt_int32,
    ECamFeatureId.MeteringAim: ECamVariantRunType.evrt_Position,
    ECamFeatureId.TriggerOption: ECamVariantRunType.evrt_TriggerOption,
    ECamFeatureId.OnePushSoftTrigger: ECamVariantRunType.evrt_voidptr,
    ECamFeatureId.MultiExposureTime: ECamVariantRunType.evrt_MultiExposureTime,
    ECamFeatureId.SignalExposureEnd: ECamVariantRunType.evrt_voidptr,
    ECamFeatureId.SignalTriggerReady: ECamVariantRunType.evrt_voidptr,
    ECamFeatureId.SignalDeviceCapture: ECamVariantRunType.evrt_voidptr,
    ECamFeatureId.ExposureOutput: ECamVariantRunType.evrt_int32,
    ECamFeatureId.OnePushTriggerCancel: ECamVariantRunType.evrt_voidptr,
    ECamFeatureId.CisPower: ECamVariantRunType.evrt_int32,
    ECamFeatureId.IrcfAdaptor: ECamVariantRunType.evrt_int32,
    ECamFeatureId.Format: ECamVariantRunType.evrt_Format,
    ECamFeatureId.RoiPosition: ECamVariantRunType.evrt_Position,
    ECamFeatureId.TriggerMode: ECamVariantRunType.evrt_int32,
    ECamFeatureId.RoiSize: ECamVariantRunType.evrt_Size,
    ECamFeatureId.Unknown: ECamVariantRunType.evrt_unknown,
}


class ECamFeatureDescType(IntEnum):
    edesc_unknown = 0
    edesc_ElementList = 1
    edesc_Range = 2
    edesc_Area = 3
    edesc_Position = 4
    edesc_Size = 5
    edesc_TriggerOption = 6
    edesc_FormatList = 7


class ECamGroupCaptureMode(IntEnum):
    egcmNoGroup = 0x00
    egcmSoftHard = 0x10
    egcmSoftSoft = 0x20


class ECamEventType(IntEnum):
    # ecetUnknown = -1
    ecetImageReceived = 0
    ecetFeatureChanged = 1
    ecetExposureEnd = 2
    ecetTriggerReady = 3
    ecetDeviceCapture = 4
    ecetAeStay = 5
    ecetAeRunning = 6
    ecetAeDisable = 7
    ecetTransError = 8
    ecetBusReset = 9
    # ecetEventTypeMax = 10


class ECamEventBusResetCode(IntEnum):
    ecebrcHappened = 1
    ecebrcRestored = 2
    ecebrcFailed = 3


class ECamNoticeType(IntEnum):
    ecntUnknown = -1
    ecntTransError = 0
    ecntGroup = 1
    ecntInfo = 2
    ecntNoticeTypeMax = 3


class ECamNoticeGroupCode(IntEnum):
    ecngcEventInsufficient = 1
    ecngcSetFeatureError = 2
    ecngcSetTransError = 3
    ecngcSoftTriggerError = 4
    ecngcSetImageFormatError = 5
    ecngcGetImageDataError = 6
    ecngcBusReset = 7


class ECamNoticeInfoCode(IntEnum):
    ecnicTemperature = 1
    ecnicComment = 2
