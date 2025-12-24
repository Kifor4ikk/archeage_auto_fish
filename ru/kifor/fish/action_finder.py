import cv2
import directkeys
import numpy as np
import pyautogui
from PIL import ImageGrab
from pyautogui import *
from directkeys import press

from ru.kifor.fish.screen_calibration import ScreenCalibration

#
image_path = "./images/"
images_and_keys = {
    "left.png": "U",
    "right.png": "I",
    "pull.png": "O",
    "release.png": "P",
    "up.png": "L"
}


class ActionFinder:

    def __init__(
            self,
            screen_calibration: ScreenCalibration
    ):
        self.screen_calibration = screen_calibration

    def _looking_for_picture(self) -> str | None:
        # Забираем экран (буквально почти скриншот) делаем его ЧБ
        for i in images_and_keys.keys():
            try:
                if pyautogui.locateOnScreen(
                        image=image_path + i,
                        region=(
                            self.screen_calibration.fishing_zone_x,
                            self.screen_calibration.fishing_zone_y,
                            self.screen_calibration.fishing_zone_x + 200,
                            self.screen_calibration.fishing_zone_y + 100
                        ),
                        confidence=0.5
                ) is not None:
                    return images_and_keys.get(i)
            except ImageNotFoundException:
                continue
        return None

    def action(self):
        while True:
            if directkeys.is_pressed("esc"):
                print("С вещами на выход")
                break

            key = self._looking_for_picture()
            print(f"Am i in? {key}")
            if key:
                directkeys.press(key)
