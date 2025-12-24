import datetime

import cv2
import numpy as np
import screeninfo
from PIL import ImageGrab
from cv2.typing import Point
from numpy.ma.core import choose
from screeninfo import Monitor


class ScreenCalibration:

    def __init__(
            self,
            screen_width: int,
            screen_height: int,
            fishing_zone_x : int,
            fishing_zone_y: int,
            monitor: Monitor
    ):
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.fishing_zone_x=fishing_zone_x
        self.fishing_zone_y=fishing_zone_y
        self.monitor = monitor

    @staticmethod
    def calibration():
        monitor = None
        while monitor is None:
            monitor = ScreenCalibration.select_monitor()
            if not monitor:
                print("Ты выбрал хуйню. Иди нахуй. Выбери нормально")
        screen = ScreenCalibration.choose_zone(monitor)
        print("Норм калибранули, ебашим!")
        return screen

    @staticmethod
    def select_monitor() -> Monitor:
        monitors = screeninfo.get_monitors()
        choice = None
        print(f"Найдено {len(monitors)} мониторов")
        for i in range(len(monitors)):
            print(f"{i}: Имя: {monitors[i].name}, W: {monitors[i].width}/ H: {monitors[i].height}")
        while choice != 0:
            choice = input("выбирай епта: ")
            try:
                return monitors[int(choice)]
            except Exception as e:
                print("Нету такого, долбаёб, выбери нормально!")
        return None

    @staticmethod
    def choose_zone(monitor: Monitor):
        print(f"Выбранная тобой хуйня: {monitor}\nДавай откалибруем твою хуйню, чтоб знать где искать твои рыбные приколы..")
        while True:
            print("Мне похуй, я беру изначально размер ЗОНЫ 150/200, а ты уже давай подбирай значения на экране")
            w = ScreenCalibration._choose_screen_pos("W")
            h = ScreenCalibration._choose_screen_pos("H")

            screen = cv2.cvtColor(
                np.array(ImageGrab.grab(bbox=(0,0, monitor.width, monitor.height))),
                cv2.COLOR_RGB2BGR
            )
            cv2.rectangle(
                screen,
                (w,h),
                ((w+200), (h+100)),
                (0,0, 255),
            )
            cv2.imshow(f'GOVNO {datetime.datetime.now()}', screen)
            print("Посмотри - норм ли(Красный квадратик). После закрой окошко и введи: 1 если заебись или любую хуйню если повторить.")
            cv2.waitKey(0)
            key = input("Вводи: ")
            if key == '1':
                print("Норм Zона, ебашим!")
                return ScreenCalibration(
                    monitor.width,
                    monitor.height,
                    w,
                    h,
                    monitor
                )

    @staticmethod
    def _choose_screen_pos(field: str) -> int:
        result = None
        while not result:
            result = input(f"Введи {field}: ")
            try:
                return int(result)
            except Exception as e:
                print("Бля, зачем ты вводишь хуйню...")
        return int(result)