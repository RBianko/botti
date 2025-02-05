from time import time

import numpy as np
import win32con
import win32gui
import win32ui


class WindowCapture:
    time = time()
    fps = 0

    def __init__(self, window_name=None):
        print("WindowCapture initialized: Window name: {}".format(window_name))
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception("Window not found: {}".format(window_name))

        window_rect = win32gui.GetWindowRect(self.hwnd)
        print("Window rect: {}".format(window_rect))

        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        self.offset_x = window_rect[0]
        self.offset_y = window_rect[1]

        border_pixels = 8
        titlebar_pixels = 30

        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.w = self.w - (border_pixels * 2)
        self.h = self.h - (titlebar_pixels + border_pixels)

    def window_capture(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt(
            (0, 0),
            (self.w, self.h),
            dcObj,
            (self.cropped_x, self.cropped_y),
            win32con.SRCCOPY,
        )

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self.h, self.w, 4)

        win32gui.DeleteObject(dataBitMap.GetHandle())
        cDC.DeleteDC()
        dcObj.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)

        img = img[..., :3]

        img = np.ascontiguousarray(img)

        return img

    def capture(self):
        self.fps = 1 / (time() - self.time)
        self.time = time()

        snapshot = self.window_capture()

        return snapshot


def list_window_names():
    window_names = []

    def callback(hwnd, ctx):
        window_names.append(win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(callback, None)
    print(window_names)

    return window_names
