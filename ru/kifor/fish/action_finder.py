
import cv2
import keyboard
import numpy as np
from PIL import ImageGrab
from pyautogui import *

from ru.kifor.fish.screen_calibration import ScreenCalibration

#
image_path = "./images/"
images_and_keys = {
    "left.png": 'V',
    "right.png": 'HOME',
    "slack.png": "END",
    "reelin.png": 'ALT+5',
    "pull.png": "DEL"
}


class ActionFinder:

    def __init__(
            self,
            screen_calibration: ScreenCalibration
    ):
        self.screen_calibration = screen_calibration
        # сделать подгрузку картинок при поднятии приложения  чтоб не читать их каждый раз

    def _looking_for_picture(self) -> str | None:
        # Забираем экран (буквально почти скриншот) делаем его ЧБ
        active_zone = cv2.cvtColor(
            np.array(ImageGrab.grab(bbox=(
                self.screen_calibration.fishing_zone_x,
                self.screen_calibration.fishing_zone_y,
                self.screen_calibration.fishing_zone_x + 200,
                self.screen_calibration.fishing_zone_y + 100))
            ),
            cv2.COLOR_BGR2RGB
        )
        for i in images_and_keys.keys():
            try:
                current_image = cv2.imread(image_path + i, cv2.COLOR_BGR2RGB)
                y = cv2.matchTemplate(image=active_zone, templ=current_image, method=cv2.TM_CCOEFF_NORMED).max()
                if y > 0.7:
                    return images_and_keys.get(i)
            except ImageNotFoundException:
                continue
        return None

    def action(self):
        while True:
            if keyboard.is_pressed("esc"):
                print("С вещами на выход")
                break
            key = self._looking_for_picture()
            if key:
                print(f"Я ПЫТАЮСЬ НАЖАТЬ {key}")
                keyboard.press_and_release(key)
                time.sleep(2)
            time.sleep(0.2)

