import datetime
import json
import threading
import time
from typing import Dict

import cv2
import keyboard
import numpy as np
from PIL import ImageGrab
from pyautogui import ImageNotFoundException
from screeninfo import Monitor, screeninfo



class Zone:
    image_path = "./images/"
    def __init__(
            self,
            name: str,
            key: str,
    ):
        self.x = 0
        self.y = 0
        self.size_x = 200
        self.size_y = 100
        self.images_and_keys = dict()
        self.threshold = 0.7
        self.name = name
        self.key = key
        self.monitor: Monitor = None
        self.delay = 4
        self.thread = None


    def _look_for_picture(self) -> str | None:
        # Забираем экран (буквально почти скриншот)
        active_zone = cv2.cvtColor(
            np.array(ImageGrab.grab(bbox=(
                self.x,
                self.y,
                self.x + self.size_x,
                self.y + self.size_y))
            ),
            cv2.COLOR_BGR2RGB
        )
        for i in self.images_and_keys.keys():
            try:
                y = cv2.matchTemplate(image=active_zone, templ=self.images_and_keys.get(i), method=cv2.TM_CCOEFF_NORMED).max()
                if y > self.threshold:
                    return i
            except ImageNotFoundException:
                print("Image was not found...")
                continue
        return None

    def _action(self):
        prev_key = None
        last_press_time = datetime.datetime.now()
        print(f"{self.name} activated. Threshold: {self.threshold} | Delay: {self.delay}")
        while True:
            if keyboard.is_pressed(self.key):
                break
            # Active work zone
            key = self._look_for_picture()
            if key:
                if prev_key != key and last_press_time + datetime.timedelta(seconds=self.delay) < datetime.datetime.now():
                    print(f"<{self.name}> try to press [{key}]")
                    last_press_time = datetime.datetime.now()
                    keyboard.press_and_release(key)
            prev_key = key

            time.sleep(0.01)

    def enable(self):
        if not self.thread:
            self.thread = threading.Thread(target=self._action())
            self.thread.start()
            return
        else:
            self.thread = None

    # Подгрузить 1 раз в прилу картинки при запуске, чтобы не прыгать каждый раз за ними на диск. Крч оптимизация епта
    def _load_images(self) -> dict:
        images_and_keys = dict()
        print("Enter keybinds file name. Exmpl: fish_binds.json")
        try:
            with open(input("Enter: "), 'rb') as f:
                data =  json.load(f)
                print(data)
            for i in data.keys():
                images_and_keys[data.get(i)]=cv2.imread(self.image_path + i, cv2.COLOR_BGR2RGB)
            self.images_and_keys = images_and_keys
            return images_and_keys
        except Exception as e:
            print(e)
            print("Cant load file")

    def _select_monitor(self) -> Monitor:
        monitors = screeninfo.get_monitors()
        print(f"Найдено {len(monitors)} мониторов")
        for i in range(len(monitors)):
            print(f"{i+1}: Name: {monitors[i].name}, Resolution: {monitors[i].width}/ {monitors[i].height}")
        while True:
            choice = input("Make a choice: ")
            try:
                self.monitor = monitors[int(choice)-1]
                return self.monitor
            except Exception as e:
                print("Wrong choose!")

    def _calibrate_zone(self):
        if not self.monitor:
            print("Current zone have no monitor!")
            return
        while True:
            w = self._choose_screen_pos("W")
            h = self._choose_screen_pos("H")
            w_size = self._choose_screen_pos("W size")
            h_size = self._choose_screen_pos("H size")

            screen = cv2.cvtColor(
                np.array(ImageGrab.grab(bbox=(0,0, self.monitor.width, self.monitor.height))),
                cv2.COLOR_RGB2BGR
            )
            cv2.rectangle(
                screen,
                (w,h),
                ((w+w_size), (h+h_size)),
                (0,0, 255),
            )
            cv2.imshow(f'CALIBRATE ZONE - {datetime.datetime.now()}', screen)
            print("Check red rectangle. If everything is ok close the window and enter 1. If u wanna choose another zone - write 0")
            cv2.waitKey(0)
            key = input("Вводи: ")
            if key == '1':
                self.x = w
                self.y = h
                self.size_x = w_size
                self.size_y = h_size
                print("Successfully saved!")
                break


    def _choose_screen_pos(self, field: str) -> int:
        result = None
        while not result:
            result = input(f"Enter {field}: ")
            try:
                return int(result)
            except Exception as e:
                print("Wrong data...")
        return int(result)

    def _set_delay_and_threshold(self):
        self.delay = int(input("Enter delay in seconds: "))
        self.threshold = int(input("Enter threshold (1-100): "))/100
        print("Done!")

    def set_setting(self):
        while True:
            print(f"Calibrating [{self.name}]"
                  f"\n1: Choose monitor"
                  f"\n2: Calibrate zone"
                  f"\n3: Set images and key binds"
                  f"\n4: Set threshold and delay"
                  f"\n0: Save and exit"
                  f"")
            enter = input("Enter: ")
            match enter:
                case "1":
                    self._select_monitor()
                case "2":
                    self._calibrate_zone()
                case "3":
                    self._load_images()
                case "4":
                    self._set_delay_and_threshold()
                case "0":
                    break
