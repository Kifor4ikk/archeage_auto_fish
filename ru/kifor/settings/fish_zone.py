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

from ru.kifor.settings.zone import Zone


class FishZone(Zone):

    image_path = "./images/"

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
                        print(f"<{self.name}> avoid key pressing [{key}] {image:}")
                        counter+=1
            # CURRENT FISH
            if last_press_time + datetime.timedelta(seconds=8) < datetime.datetime.now() and not notify_fish_killed:
                if start_fishing_time:
                    took_time = datetime.datetime.now() - start_fishing_time - datetime.timedelta(seconds=8)
                    print(f"Fish killed! Took {took_time.seconds} seconds.\n")
                    start_fishing_time = None
                    # self._press_key("U")
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
