import win32api, win32con, win32gui
from ctypes import *
from threading import Thread
import time

#
# Device change events (WM_DEVICECHANGE wParam)
#
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEQUERYREMOVE = 0x8001
DBT_DEVICEQUERYREMOVEFAILED = 0x8002
DBT_DEVICEMOVEPENDING = 0x8003
DBT_DEVICEREMOVECOMPLETE = 0x8004
DBT_DEVICETYPESSPECIFIC = 0x8005
DBT_CONFIGCHANGED = 0x0018

#
# type of device in DEV_BROADCAST_HDR
#
DBT_DEVTYP_OEM = 0x00000000
DBT_DEVTYP_DEVNODE = 0x00000001
DBT_DEVTYP_VOLUME = 0x00000002
DBT_DEVTYPE_PORT = 0x00000003
DBT_DEVTYPE_NET = 0x00000004

#
# media types in DBT_DEVTYP_VOLUME
#
DBTF_MEDIA = 0x0001
DBTF_NET = 0x0002

WORD = c_ushort
DWORD = c_ulong


class DEV_BROADCAST_HDR(Structure):
    _fields_ = [
        ("dbch_size", DWORD),
        ("dbch_devicetype", DWORD),
        ("dbch_reserved", DWORD)
    ]


class DEV_BROADCAST_VOLUME(Structure):
    _fields_ = [
        ("dbcv_size", DWORD),
        ("dbcv_devicetype", DWORD),
        ("dbcv_reserved", DWORD),
        ("dbcv_unitmask", DWORD),
        ("dbcv_flags", WORD)
    ]


def drive_from_mask(mask):
    n_drive = 0
    while 1:
        if (mask & (2 ** n_drive)):
            return n_drive
        else:
            n_drive += 1


class Notification:
    def __init__(self):
        message_map = {
            win32con.WM_DEVICECHANGE: self.onDeviceChange,
            win32con.WM_QUIT: self.onDeviceChange,
        }

        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "NAWCScannerDetection"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(
            classAtom,
            "NAWC Scanner Detection",
            style,
            0, 0,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0, 0,
            hinst, None
        )

    def register_callbacks(self, device_arrival, device_removal):
        self.dvc_arr = device_arrival
        self.dvc_rem = device_removal

    def onDeviceChange(self, hwnd, msg, wparam, lparam):
        #
        # WM_DEVICECHANGE:
        #  wParam - type of change: arrival, removal etc.
        #  lParam - what's changed?
        #    if it's a volume then...
        #  lParam - what's changed more exactly
        #
        dev_broadcast_hdr = DEV_BROADCAST_HDR.from_address(lparam)
        if wparam == DBT_DEVICEARRIVAL:
            if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYP_VOLUME:                
                dev_broadcast_volume = DEV_BROADCAST_VOLUME.from_address(lparam)
                drive_letter = drive_from_mask(dev_broadcast_volume.dbcv_unitmask)
                self.dvc_arr(chr(ord("A") + drive_letter))

        if wparam == DBT_DEVICEREMOVECOMPLETE:
            self.dvc_rem()

        return 1


def listener_thread(clb_arr, clb_rem):
    w = Notification()
    w.register_callbacks(clb_arr, clb_rem)
    win32gui.PumpMessages()


def create_listener(clb_arr, clb_rem):
    thread = Thread(target = listener_thread, args=(clb_arr, clb_rem))
    thread.start()
    return thread


if __name__ == '__main__':
    print("Starting listening")
    w = Notification()
    win32gui.PumpMessages()