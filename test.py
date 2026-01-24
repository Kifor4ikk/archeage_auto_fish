import json
import time
from email.charset import BASE64

import playsound
def get_data() -> (int, int):
    with open("C:\\Users\kifor\Documents\AAClassic\Addon\info.json",'rb') as f:
        data =  bytes.decode(f.read(), 'UTF-8')
        data = data.replace("\"", "")
        data = data.split(",")
        if data:

        return data[0], data[1]

if __name__ == "__main__":
    while(True):
        time.sleep(0.2)
        print(get_data())
