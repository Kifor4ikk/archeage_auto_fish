import os

import cv2
from screeninfo import screeninfo

from ru.kifor.fish.action_finder import ActionFinder
from ru.kifor.fish.screen_calibration import ScreenCalibration

def menu():
    action: ActionFinder = None
    screen: ScreenCalibration = None
    x = None
    while x != "0":

        print("------------------")
        print("Здарова заебал, выбирай:\n1: Калибровка монитора\n2:Калибровка зоны фишинга\n3:Работаем братья\n0: Пошел нахуй")
        x = input("Введи говна: ")
        print(f"Вы ввели говна: {x}")
        match x:
            case '1':
                print("Калибруем ваше дерьмо")
                screen = ScreenCalibration.calibration()
                action = ActionFinder(screen)
            case '2':
                print("Калибровка каллом.")
                if not screen:
                    print("Не, нихуя, сначала откалибруй своё дерьмо (Пункт 1)")
                else:
                    screen = ScreenCalibration.choose_zone(screen.monitor)
                    action = ActionFinder(screen)
            case '3':
                print("Нажми ESC если надо остановиться!")
                if not action:
                    print("Ебать, а ты экранчик то калибранул, убежище?")
                else:
                    action.action()
            case '0':
                print("Давай, иди нахуй")
                break

if __name__ == '__main__':
    menu()
    # picture = cv2.imread("./images/left.png")
    # picture = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    #
    # cv2.imshow("penis", picture)
    # cv2.waitKey(0)

