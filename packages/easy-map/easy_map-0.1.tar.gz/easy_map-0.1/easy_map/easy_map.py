from PIL import Image
import requests
from io import BytesIO

class easy_map:

    def __init__(self, key, log = False, **kwargs):
        self.key = key
        self.data = kwargs
        self.log = log

    def get_image(self, map_type):
        url = "https://dev.virtualearth.net/REST/V1/Imagery/Map/" + map_type + "?"
        for key, value in self.data.items():
            print(key,value)
            if (key == "mapArea"):
                url += "mapArea={},{},{},{}".format(*value) + "&"
            else:
                url += key + "=" + value + "&"
        url += "key=" + self.key

        if self.log:
            print(url)

        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def get_meta(self, map_type):
        url = "https://dev.virtualearth.net/REST/V1/Imagery/Map/" + map_type + "?mapMetadata=1&"
        for key, value in self.data.items():
            print(key, value)
            if (key == "mapArea"):
                url += "mapArea={},{},{},{}".format(*value) + "&"
            else:
                url += key + "=" + value + "&"
        url += "key=" + self.key

        if self.log:
            print(url)

        return requests.get(url).json()
