import sys
import threading

import cv2
import keyboard

from ru.kifor.settings.fish_zone import FishZone
from ru.kifor.settings.save_settings import load_data, save_data
from ru.kifor.settings.settings import Settings
from ru.kifor.settings.zone import Zone


def create_new_zone() -> Zone:
    name = input("Enter name: ")
    key = input("Enter active key name. (Exmpl F12) \nEnter: ")
    choice = input("Choose zone type\n1: Basic zone\n2: Fishing zone\nEnter: ")

    match choice:
        case "1":
            return Zone(
                name=name,
                key=key
            )
        case "2":
            return FishZone(
                name=name,
                key=key
            )
    raise ValueError("Wrong choice")





def menu(settings: Settings | None):
    if not settings:
        settings = Settings()
    while True:
        print("Yo! Create zone or smth\n"
              "1: Create new zone\n"
              "2: Choose choose and rebuild another zone\n"
              "3: Save zones\n"
              "4: Delete zone by key\n"
              "5: Activate/Disable zone\n"
              "0: Exit\n"
              "-------------------\n"
              "Zones exists\n"
              "-------------------"
              )
        for z in range(len(settings.zones)):
            print(f"{settings.zones[z].name} - [{settings.zones[z].key}] - [{'Active' if settings.zones[z].thread is not None else 'Disabled'}] [hwnd: {settings.zones[z].hwnd} Window:{settings.zones[z].window_name}]")
        print("-------------------")
        choice = input("Enter: ")
        match choice:
            case "1":
                zone = create_new_zone()
                zone.set_setting()
                settings.zones.append(zone)
                print("Zone was saved in settings!")
            case "2":
                for z in range(len(settings.zones)):
                    print(f"{z+1}: {settings.zones[z].name} - [{settings.zones[z].key}]")
                settings.zones[int((input("Enter: ")))-1].set_setting()
            case "3":
                save_data(settings)
                print("saved")
            case "4":
                x  = input("Input zone key to delete: ")
                for z in settings.zones:
                    print(f"{z.key} - {x}" )
                    if z.key == x:
                        settings.zones.remove(z)
            case "5":
                x = input("Input KEY to activate ZONE checking: ")
                for z in settings.zones:
                    if z.key == x:
                        z.enable()
            case "0":
                print("\nSee ya!")
                return



def test():
    zone = cv2.imread("images/screen.png")
    skill_good = cv2.imread("images/reelin.png")
    skill_bad = cv2.imread("images/right.png")
    x = cv2.matchTemplate(skill_good, zone, cv2.TM_CCOEFF_NORMED).max()
    y = cv2.matchTemplate(skill_bad, zone , cv2.TM_CCOEFF_NORMED).max()
    print(f"Good data {round(x*100)}%. {'Fine! 'if x > 0.75 else 'Mm smth is wrong.' }")
    print(f"Bad data {round(y*100)}%. {'Fine!' if y < 0.5 else 'A lot of thresholds'}")

if __name__ == '__main__':
    sys.path.append("./*")
    test()
    menu(load_data())

