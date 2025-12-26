import os
import pickle

from ru.kifor.fish.action_finder import ActionFinder


def load_data() -> ActionFinder | None:
    if os.path.exists("save.piska"):
        with open("save.piska", "rb") as f:
            return pickle.load(f)
    else:
        print("Нету файла сохранения")
        return None

def save_data(action: ActionFinder):
    try:
        with open("save.piska", "wb") as f:
            pickle.dump(action, f, protocol=None)
    except Exception as e:
        print("Не смог сохранить твою хуйню..")