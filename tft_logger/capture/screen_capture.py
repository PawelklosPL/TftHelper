# screen_capture.py
from dataclasses import dataclass

import mss
from PIL import Image


@dataclass
class ScreenCapture:
    monitor_index: int = 1

    def __post_init__(self):
        self._sct = mss.mss()

    def grab_region(self, region):
        left, top, width, height = region
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "mon": self.monitor_index,
        }

        sct_img = self._sct.grab(monitor)
        # mss zwraca raw, konwertujemy na PIL.Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        return img
