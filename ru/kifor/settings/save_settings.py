import os
import pickle

from ru.kifor.settings.settings import Settings


def load_data() -> Settings | None:
    if os.path.exists("save.piska"):
        with open("save.piska", "rb") as f:
            return pickle.load(f)
    else:
        print("Нету файла сохранения")
        return None

def save_data(setting: Settings):
    try:
        with open("save.piska", "wb") as f:
            pickle.dump(setting, f, protocol=None)
    except Exception as e:
        print("Cant save ur shit..")