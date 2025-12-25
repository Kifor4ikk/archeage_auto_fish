import os
import sys

import cv2
from ru.kifor.fish.action_finder import ActionFinder
from ru.kifor.fish.screen_calibration import ScreenCalibration
def menu():
    screen: ScreenCalibration = ScreenCalibration(
    3440, 1440, 2250,800,
        monitor=None
    )
    action: ActionFinder = ActionFinder(screen)

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

def test() -> bool:
    zone = cv2.imread("images/screen.png")
    skill_da = cv2.imread("images/reelin.png")
    skill_net = cv2.imread("images/right.png")

    x = cv2.matchTemplate(skill_da, zone, cv2.TM_CCOEFF_NORMED).max()
    y = cv2.matchTemplate(skill_net, zone , cv2.TM_CCOEFF_NORMED).max()
    return x > 0.7 > y

if __name__ == '__main__':
    sys.path.append("./*")
    # print(os.getcwd())
    if test():
        menu()
    else:
        print("Пососи писос. Поделай скринов из своей игры и положи в папочку, возможно роляет разрешение экрана")

