import base64
import ctypes
import io
import sys
import threading
from ctypes import wintypes

from PIL import Image
import pystray

APP_NAME = "TPowerPlanSwitcher"

BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"
POWER_SAVER_GUID = "a1841308-3541-4fab-bc81-f71556f20b4a"

PLAN_NAMES = {
    BALANCED_GUID: "Balanced",
    POWER_SAVER_GUID: "Power saver",
}

ICON_POWER_SAVER_B64 = (
    "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"
    "AElFTkSuQmCC"
)

ICON_BALANCED_B64 = (
    "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"
    "QmCC"
)


def _decode_icon(data: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(data))).convert("RGBA")


PLAN_ICONS = {
    BALANCED_GUID: _decode_icon(ICON_BALANCED_B64),
    POWER_SAVER_GUID: _decode_icon(ICON_POWER_SAVER_B64),
}


if sys.platform == "win32":
    powrprof = ctypes.WinDLL("powrprof", use_last_error=True)
    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    ole32 = ctypes.WinDLL("ole32", use_last_error=True)


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]


PGUID = ctypes.POINTER(GUID)
HKEY = ctypes.c_void_p

powrprof.PowerGetActiveScheme.argtypes = [HKEY, ctypes.POINTER(PGUID)]
powrprof.PowerGetActiveScheme.restype = wintypes.DWORD
powrprof.PowerSetActiveScheme.argtypes = [HKEY, PGUID]
powrprof.PowerSetActiveScheme.restype = wintypes.DWORD

ole32.StringFromGUID2.argtypes = [PGUID, wintypes.LPWSTR, ctypes.c_int]
ole32.StringFromGUID2.restype = ctypes.c_int
ole32.CLSIDFromString.argtypes = [wintypes.LPCWSTR, PGUID]
ole32.CLSIDFromString.restype = ctypes.c_long

kernel32.LocalFree.argtypes = [ctypes.c_void_p]
kernel32.LocalFree.restype = ctypes.c_void_p
kernel32.CreateEventW.argtypes = [
    ctypes.c_void_p,
    wintypes.BOOL,
    wintypes.BOOL,
    wintypes.LPCWSTR,
]
kernel32.CreateEventW.restype = wintypes.HANDLE
kernel32.SetEvent.argtypes = [wintypes.HANDLE]
kernel32.SetEvent.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL
kernel32.WaitForMultipleObjects.argtypes = [
    wintypes.DWORD,
    ctypes.POINTER(wintypes.HANDLE),
    wintypes.BOOL,
    wintypes.DWORD,
]
kernel32.WaitForMultipleObjects.restype = wintypes.DWORD

advapi32.RegOpenKeyExW.argtypes = [
    HKEY,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.POINTER(HKEY),
]
advapi32.RegOpenKeyExW.restype = wintypes.LONG
advapi32.RegNotifyChangeKeyValue.argtypes = [
    HKEY,
    wintypes.BOOL,
    wintypes.DWORD,
    wintypes.HANDLE,
    wintypes.BOOL,
]
advapi32.RegNotifyChangeKeyValue.restype = wintypes.LONG
advapi32.RegCloseKey.argtypes = [HKEY]
advapi32.RegCloseKey.restype = wintypes.LONG

HKEY_LOCAL_MACHINE = HKEY(0x80000000)
POWER_SCHEMES_KEY = r"SYSTEM\CurrentControlSet\Control\Power\User\PowerSchemes"

KEY_NOTIFY = 0x0010
REG_NOTIFY_CHANGE_LAST_SET = 0x00000004
INFINITE = 0xFFFFFFFF
WAIT_OBJECT_0 = 0
ERROR_SUCCESS = 0
ERROR_ALREADY_EXISTS = 183


def get_active_scheme():
    pointer = PGUID()
    if powrprof.PowerGetActiveScheme(None, ctypes.byref(pointer)) != ERROR_SUCCESS:
        return None
    try:
        buffer = ctypes.create_unicode_buffer(64)
        if ole32.StringFromGUID2(pointer, buffer, 64) == 0:
            return None
        return buffer.value.strip("{}").lower()
    finally:
        kernel32.LocalFree(pointer)


def set_active_scheme(guid: str) -> bool:
    parsed = GUID()
    if ole32.CLSIDFromString("{%s}" % guid, ctypes.byref(parsed)) != 0:
        return False
    return powrprof.PowerSetActiveScheme(None, ctypes.byref(parsed)) == ERROR_SUCCESS


class PowerPlanSwitcher:
    def __init__(self):
        self.active = get_active_scheme() or POWER_SAVER_GUID
        self.stop_event = kernel32.CreateEventW(None, True, False, None)

        self.icon = pystray.Icon(
            APP_NAME,
            icon=self._current_icon(),
            title=self._tooltip(),
            menu=self._build_menu(),
        )

    def _current_icon(self):
        return PLAN_ICONS.get(self.active, PLAN_ICONS[POWER_SAVER_GUID])

    def _tooltip(self):
        return "Power Mode - Active: {}".format(
            PLAN_NAMES.get(self.active, "Other plan")
        )

    def _build_menu(self):
        return pystray.Menu(
            pystray.MenuItem(
                "Toggle", self._on_toggle, default=True, visible=False
            ),
            pystray.MenuItem(
                PLAN_NAMES[POWER_SAVER_GUID],
                self._select(POWER_SAVER_GUID),
                checked=lambda item: self.active == POWER_SAVER_GUID,
                radio=True,
            ),
            pystray.MenuItem(
                PLAN_NAMES[BALANCED_GUID],
                self._select(BALANCED_GUID),
                checked=lambda item: self.active == BALANCED_GUID,
                radio=True,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._on_exit),
        )

    def _refresh(self):
        self.icon.icon = self._current_icon()
        self.icon.title = self._tooltip()
        self.icon.update_menu()

    def _apply(self, guid: str):
        if set_active_scheme(guid):
            self.active = guid
        else:
            self.active = get_active_scheme() or self.active
            self.icon.notify(
                "Could not change the power plan. "
                "It may be restricted on this PC.",
                APP_NAME,
            )
        self._refresh()

    def _select(self, guid: str):
        def handler(icon, item):
            self._apply(guid)

        return handler

    def _on_toggle(self, icon, item):
        target = (
            POWER_SAVER_GUID if self.active == BALANCED_GUID else BALANCED_GUID
        )
        self._apply(target)

    def _on_exit(self, icon, item):
        kernel32.SetEvent(self.stop_event)
        icon.stop()

    def _watch(self):
        key = HKEY()
        if (
            advapi32.RegOpenKeyExW(
                HKEY_LOCAL_MACHINE,
                POWER_SCHEMES_KEY,
                0,
                KEY_NOTIFY,
                ctypes.byref(key),
            )
            != ERROR_SUCCESS
        ):
            return

        change_event = kernel32.CreateEventW(None, False, False, None)
        handles = (wintypes.HANDLE * 2)(self.stop_event, change_event)

        try:
            while True:
                if (
                    advapi32.RegNotifyChangeKeyValue(
                        key,
                        False,
                        REG_NOTIFY_CHANGE_LAST_SET,
                        change_event,
                        True,
                    )
                    != ERROR_SUCCESS
                ):
                    return

                result = kernel32.WaitForMultipleObjects(
                    2, handles, False, INFINITE
                )
                if result != WAIT_OBJECT_0 + 1:
                    return

                current = get_active_scheme()
                if current and current != self.active:
                    self.active = current
                    self._refresh()
        finally:
            kernel32.CloseHandle(change_event)
            advapi32.RegCloseKey(key)

    def run(self):
        threading.Thread(target=self._watch, daemon=True).start()
        try:
            self.icon.run()
        finally:
            kernel32.SetEvent(self.stop_event)
            kernel32.CloseHandle(self.stop_event)


def enable_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except Exception:
        pass
    try:
        user32.SetProcessDPIAware()
    except Exception:
        pass


def is_single_instance() -> bool:
    kernel32.CreateMutexW(None, False, APP_NAME + "_Mutex")
    return kernel32.GetLastError() != ERROR_ALREADY_EXISTS


def main():
    if sys.platform != "win32":
        print("This application only runs on Windows.")
        return 1
    if not is_single_instance():
        return 0
    enable_dpi_awareness()
    PowerPlanSwitcher().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
