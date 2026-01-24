import datetime
import json
import threading
import time
from threading import activeCount
from typing import Dict

import cv2
import keyboard
import numpy as np
import playsound
import pyautogui
import pydub.playback
import win32api
import win32con
import winsound
from PIL import ImageGrab
from pyautogui import ImageNotFoundException
from pydub import AudioSegment
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
        self.key_and_image_name = dict()
        self.threshold = 0.7
        self.name = name
        self.key = key
        self.monitor: Monitor = None
        self.delay = 4
        self.thread = None
        self.window_name = None
        self.hwnd = None

    def _get_picture(self):
        if self.hwnd:
            return cv2.cvtColor(
                np.array(ImageGrab.grab(
                    bbox=(self.x, self.y, self.x + self.size_x, self.y + self.size_y),
                    window=self.hwnd
                )),
                cv2.COLOR_BGR2RGB
            )
        else:
            return cv2.cvtColor(
                np.array(ImageGrab.grab(bbox=(self.x, self.y, self.x + self.size_x, self.y + self.size_y))),
                cv2.COLOR_BGR2RGB
            )


    def _look_for_picture(self) -> (str | None, str | None):
        # Забираем экран (буквально почти скриншот)
        active_zone = self._get_picture()
        for i in self.images_and_keys.keys():
            try:
                y = cv2.matchTemplate(image=active_zone, templ=self.images_and_keys.get(i), method=cv2.TM_CCOEFF_NORMED).max()
                if y > self.threshold:
                    return i, self.key_and_image_name.get(i)
            except ImageNotFoundException:
                print("Image was not found...")
                continue
        return None, None

    def _action(self):
        prev_key = None
        last_press_time = datetime.datetime.now()

        start_fishing_time = None
        notify_fish_killed = False

        global_fishing_time = None
        notify_global_killing = False

        fish_time_counter = []

        counter = 0
        print(f"{self.name} activated. Threshold: {self.threshold} | Delay: {self.delay}")
        while True:
            if keyboard.is_pressed(self.key):
                break
            # Active work zone
            key, image = self._look_for_picture()
            if key:
                if prev_key != key and last_press_time + datetime.timedelta(seconds=self.delay) < datetime.datetime.now():
                    notify_fish_killed = False
                    notify_global_killing = False
                    last_press_time = datetime.datetime.now()
                    # ------------ just counting
                    if start_fishing_time is None:
                        start_fishing_time = datetime.datetime.now()
                    if global_fishing_time is None:
                        global_fishing_time = datetime.datetime.now()

                    # Try to avoid
                    if counter > 3 or image in ['reelin.png', 'pull.png']:
                        print(f"<{self.name}> try to press [{key}] {image if image in ['reelin.png', 'pull.png'] else ''}")
                        self._press_key(key)
                        counter = 0
                    else:
                        print(f"<{self.name}> avoid key pressing [{key}] {image}")
                        counter+=1
            # CURRENT FISH
            if last_press_time + datetime.timedelta(seconds=8) < datetime.datetime.now() and not notify_fish_killed:
                if start_fishing_time:
                    took_time = datetime.datetime.now() - start_fishing_time - datetime.timedelta(seconds=8)
                    print(f"Fish killed! Took {took_time.seconds} seconds.\n")
                    start_fishing_time = None
                    self._press_key("U")
                    notify_fish_killed = True
                    fish_time_counter.append(took_time.seconds)
                    try:
                        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    except Exception as e:
                        print("CANT PLAY SOUND")
            # GLOBAL
            if last_press_time + datetime.timedelta(seconds=60) < datetime.datetime.now() and not notify_global_killing:
                if global_fishing_time:
                    print(f"Fishing end! You got {len(fish_time_counter)} fishes! Average fishing time {self._average_fishing_time(fish_time_counter)}")
                    print(f"Fishing took {(datetime.datetime.now() - global_fishing_time).seconds}")
                    global_fishing_time = None
                    notify_global_killing = True
                    fish_time_counter = []

            prev_key = key
            time.sleep(0.01)

    def _average_fishing_time(self, array_of_times):
        summ = 0
        for t in array_of_times:
            summ+=t
        return summ/len(array_of_times)

    def _press_key(self, key):
        if self.hwnd:
            win32api.PostMessage(self.hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
            win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, ord(key), 0)
            win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, ord(key), 0)
        else:
            keyboard.press_and_release(key)

    def _set_new_hwnd(self) -> str:
        winds = pyautogui.getAllWindows()
        if self.window_name and self.hwnd:
            for x in winds:
                if x._hWnd == self.hwnd:
                    return self.hwnd
            for x in winds:
                if x.title == self.window_name:
                    return x._hWnd
        return None

    def enable(self):
        self.hwnd = self._set_new_hwnd()
        if not self.thread:
            self.thread = threading.Thread(target=self._action())
            self.thread.start()
            return
        else:
            self.thread = None

    # Подгрузить 1 раз в прилу картинки при запуске, чтобы не прыгать каждый раз за ними на диск. Крч оптимизация епта
    def _load_images(self) -> dict:
        self.images_and_keys = dict()
        self.key_and_image_name = dict()
        print("Enter keybinds file name. Exmpl: fish_binds.json")
        try:
            with open(input("Enter: "), 'rb') as f:
                data =  json.load(f)
                print(data)
            for i in data.keys():
                self.images_and_keys[data.get(i)]=cv2.imread(self.image_path + i, cv2.COLOR_BGR2RGB)
                self.key_and_image_name[data.get(i)]=i
            return self.images_and_keys
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

    def _set_window(self):
        print("Choose window working for ")
        windws = pyautogui.getAllWindows()
        for i in range(0, len(windws)):
            print(f"{i+1}: {windws[i]._hWnd} - {windws[i].title} ")
        x = int(input("Enter: "))
        try:
            self.hwnd = windws[x-1]._hWnd
            self.window_name = windws[x-1].title
        except Exception as e:
            print(e)
            print('Ты ошибка природы')
            return
    def _show_active_zone(self):
        screen = cv2.cvtColor(
            np.array(ImageGrab.grab(bbox=(0,0, self.monitor.width, self.monitor.height))),
            cv2.COLOR_RGB2BGR
        )
        cv2.rectangle(
            screen,
            (self.x,self.y),
            ((self.x+self.size_x), (self.y+self.size_y)),
            (0,0, 255),
        )
        cv2.imshow(f'CALIBRATE ZONE - {datetime.datetime.now()}', screen)
        cv2.waitKey(0)

    def set_setting(self):
        while True:
            print(f"Calibrating [{self.name}]"
                  f"\n1: Choose monitor"
                  f"\n2: Calibrate zone"
                  f"\n3: Set images and key binds"
                  f"\n4: Set threshold and delay"
                  f"\n5: Set active window"
                  f"\n6: Show active zone"
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
                case "5":
                    self._set_window()
                case "6":
                    self._show_active_zone()
                case "0":
                    break
