import io
import json
import os
import pickle
import sys
import time

import cv2
from ru.kifor.fish.action_finder import ActionFinder
from ru.kifor.fish.screen_calibration import ScreenCalibration
from ru.kifor.settings.save_settings import save_data, load_data

def load_key_binds() -> dict:
    with open("keybinds.json", 'rb') as f:
        keys = json.load(f)
        if len(keys.keys()) != 5:
            raise Exception("У вас дохлый файл настроек кейбиндов")
        return keys

def menu(act: ActionFinder | None):
    key_binds = load_key_binds()
    screen: ScreenCalibration = None
    action: ActionFinder = None
    if act:
        action = act
        screen = act.screen_calibration
    else:
        print("Йоу мне тут птица напела, что у тебя не откалиброван моник, давай уже постарайся сделать своё грязное дело")

    x = None
    while x != "0":

        print("------------------")
        print("Здарова заебал, выбирай:\n"
              "1:Калибровка монитора(Включает в себя калибровку зоны фишинга)\n"
              "2:Калибровка зоны фишинга\n"
              "3:Работаем братья\n"
              "4:Изменение пороговых значений для поиска картинки\n"
              "8:Сохрани настройки\n"
              "0: Пошел нахуй")
        x = input("Введи говна: ")
        print(f"Вы ввели говна: {x}")
        match x:
            case '1':
                print("Калибруем ваше дерьмо")
                screen = ScreenCalibration.calibration()
                if action is not None:
                    action.screen_calibration = screen
                else:
                    action = ActionFinder(screen, key_binds=key_binds)
            case '2':
                print("Калибровка каллом.")
                if not screen:
                    print("Не, нихуя, сначала откалибруй своё дерьмо (Пункт 1)")
                else:
                    screen = ScreenCalibration.choose_zone(screen.monitor)
                    if action is not None:
                        action.screen_calibration = screen
                    else:
                        action = ActionFinder(screen, key_binds=key_binds)
            case '3':
                print("Нажми ESC если надо остановиться!")
                if not action:
                    print("Ебать, а ты экранчик то калибранул, убежище?")
                else:
                    action.action()
            case '4':
                if action:
                    x = int(input("Вводи желамое значение: "))
                    if x <= 0 or x > 100:
                        print("Дуралей...")
                    else:
                        action.threshold = x/100
                else:
                    print("Калбируйся сперва.")

            case '8':
                print("Сохранить нынешние настройки")
                save_data(action)
            case '0':
                print("Давай, иди нахуй")
                break

def test() -> bool:
    zone = cv2.imread("images/screen.png")
    skill_good = cv2.imread("images/reelin.png")
    skill_bad = cv2.imread("images/right.png")

    x = cv2.matchTemplate(skill_good, zone, cv2.TM_CCOEFF_NORMED).max()
    y = cv2.matchTemplate(skill_bad, zone , cv2.TM_CCOEFF_NORMED).max()
    print(f"Правильную картинку распознало с порогом {round(x*100)}%. {'Всё пиздато 'if x > 0.75 else 'Ну.. Хуеватенько.' }")
    print(f"Не правильную картинку распознало с порогом {round(y*100)}%. {'Заебумба' if y < 0.5 else 'Слишком много, но главное чтобы ваш установленный порог оно не перешагивало'}")

if __name__ == '__main__':
    sys.path.append("./*")
    test()
    menu(load_data())

