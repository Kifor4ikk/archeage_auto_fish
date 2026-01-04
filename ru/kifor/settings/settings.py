from typing import List

from ru.kifor.settings.zone import Zone


class Settings:

    def __init__(self):
        self.zones: List[Zone] = []