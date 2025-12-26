
import cv2
import keyboard
import numpy as np
from PIL import ImageGrab
from pyautogui import *

from ru.kifor.fish.screen_calibration import ScreenCalibration

#
image_path = "./images/"

class ActionFinder:

    def __init__(
            self,
            screen_calibration: ScreenCalibration,
            key_binds: dict,
            threshold = 0.7,
    ):
        self.screen_calibration = screen_calibration
        self.threshold = threshold
        self.images_and_keys = self._load_images(key_binds)

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
        for i in self.images_and_keys.keys():
            try:

                y = cv2.matchTemplate(image=active_zone, templ=self.images_and_keys.get(i), method=cv2.TM_CCOEFF_NORMED).max()
                if y > self.threshold:
                    return i
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

    # Подгрузить 1 раз в прилу картинки при запуске, чтобы не прыгать каждый раз за ними на диск. Крч оптимизация епта
    def _load_images(self, key_binds: dict) -> dict:
        images_and_keys: dict = dict()
        for i in key_binds.keys():
            images_and_keys[key_binds.get(i)]=cv2.imread(image_path + i, cv2.COLOR_BGR2RGB)
        return images_and_keys