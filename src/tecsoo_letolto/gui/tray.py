from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes


class WindowsTrayIcon:
    def __init__(self, hwnd: int, tooltip: str) -> None:
        self._hwnd = hwnd
        self._tooltip = tooltip
        self._active = False
        self._callback = None
        self._old_wndproc = None
        self._restore_requested = False

    def show(self) -> bool:
        if sys.platform != "win32" or self._active:
            return False
        shell32 = ctypes.windll.shell32
        user32 = ctypes.windll.user32
        nid = _notify_icon_data(self._hwnd, self._tooltip)
        if not shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid)):
            return False
        self._install_wndproc(user32)
        self._active = True
        return True

    @property
    def active(self) -> bool:
        return self._active

    def consume_restore_request(self) -> bool:
        requested = self._restore_requested
        self._restore_requested = False
        return requested

    def remove(self) -> None:
        if sys.platform != "win32" or not self._active:
            return
        shell32 = ctypes.windll.shell32
        user32 = ctypes.windll.user32
        if self._old_wndproc:
            _set_window_long_ptr(user32, self._hwnd, GWLP_WNDPROC, self._old_wndproc)
            self._old_wndproc = None
            self._callback = None
        nid = _notify_icon_data(self._hwnd, self._tooltip)
        shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(nid))
        self._active = False

    def _install_wndproc(self, user32) -> None:
        if self._callback is not None:
            return

        @WNDPROC
        def wndproc(hwnd, msg, wparam, lparam):
            if msg == WM_TRAYICON and lparam in (WM_LBUTTONUP, WM_LBUTTONDBLCLK, WM_RBUTTONUP):
                self._restore_requested = True
                return 0
            return user32.CallWindowProcW(self._old_wndproc, hwnd, msg, wparam, lparam)

        self._callback = wndproc
        _configure_user32_window_proc(user32)
        self._old_wndproc = _set_window_long_ptr(user32, self._hwnd, GWLP_WNDPROC, self._callback)


class NOTIFYICONDATAW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HICON),
        ("szTip", wintypes.WCHAR * 128),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("szInfo", wintypes.WCHAR * 256),
        ("uVersion", wintypes.UINT),
        ("szInfoTitle", wintypes.WCHAR * 64),
        ("dwInfoFlags", wintypes.DWORD),
    ]


NIM_ADD = 0
NIM_DELETE = 2
NIF_MESSAGE = 1
NIF_ICON = 2
NIF_TIP = 4
WM_USER = 0x0400
WM_TRAYICON = WM_USER + 20
WM_LBUTTONUP = 0x0202
WM_LBUTTONDBLCLK = 0x0203
WM_RBUTTONUP = 0x0205
GWLP_WNDPROC = -4
IDI_APPLICATION = 32512
LONG_PTR = ctypes.c_longlong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_long
WNDPROC = ctypes.WINFUNCTYPE(LONG_PTR, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)


def _notify_icon_data(hwnd: int, tooltip: str) -> NOTIFYICONDATAW:
    user32 = ctypes.windll.user32
    user32.LoadIconW.restype = wintypes.HICON
    data = NOTIFYICONDATAW()
    data.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
    data.hWnd = hwnd
    data.uID = 1
    data.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
    data.uCallbackMessage = WM_TRAYICON
    data.hIcon = user32.LoadIconW(None, IDI_APPLICATION)
    data.szTip = tooltip[:127]
    return data


def _configure_user32_window_proc(user32) -> None:
    user32.CallWindowProcW.argtypes = [LONG_PTR, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.CallWindowProcW.restype = LONG_PTR


def _window_proc_pointer(callback_or_pointer) -> int:
    if isinstance(callback_or_pointer, int):
        return callback_or_pointer
    pointer = ctypes.cast(callback_or_pointer, ctypes.c_void_p).value
    if pointer is None:
        raise ValueError("Window procedure pointer is not available.")
    return pointer


def _set_window_long_ptr(user32, hwnd: int, index: int, callback_or_pointer):
    pointer = _window_proc_pointer(callback_or_pointer)
    if hasattr(user32, "SetWindowLongPtrW"):
        user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, LONG_PTR]
        user32.SetWindowLongPtrW.restype = LONG_PTR
        return user32.SetWindowLongPtrW(hwnd, index, pointer)
    user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, LONG_PTR]
    user32.SetWindowLongW.restype = LONG_PTR
    return user32.SetWindowLongW(hwnd, index, pointer)
