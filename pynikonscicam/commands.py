import ctypes

from . import methods as m
from . import constants as c
from . import structures as s
from . import error_codes as e


def get_frame_size(camera_handle: int):
    """Get the frame size of the camera."""
    frame_size = s.CAM_CMD_GetFrameSize()
    m.send_command(camera_handle, c.CAM_CMD_GET_FRAMESIZE, ctypes.byref(frame_size))

    return frame_size


def start_frame_transfer(camera_handle: int, image_buffer_num: int = 1) -> None:
    """Start frame transfer."""
    start_frame_transfer_struct = s.CAM_CMD_StartFrameTransfer()
    start_frame_transfer_struct.uiImageBufferNum = image_buffer_num
    m.send_command(camera_handle, c.CAM_CMD_START_FRAMETRANSFER, ctypes.byref(start_frame_transfer_struct))
    # TODO Check for memory allocation errors, see SDK documentation


def stop_frame_transfer(camera_handle: int) -> None:
    """Stop frame transfer."""
    error_code = m.send_command(camera_handle, c.CAM_CMD_STOP_FRAMETRANSFER, None)
