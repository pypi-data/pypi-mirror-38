from PIL import Image
import requests
from io import BytesIO

class easy_map:

    def __init__(self, key, map_type, log = False, **kwargs):
        self.key = key
        self.data = kwargs
        self.log = log
        self.map_type = map_type

    def get_image(self):
        url = "https://dev.virtualearth.net/REST/V1/Imagery/Map/" + self.map_type + "?"
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

    def get_meta(self):
        url = "https://dev.virtualearth.net/REST/V1/Imagery/Map/" + self.map_type + "?mapMetadata=1&"
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

    def get_bounding_Box(self):
        meta = self.get_meta()
        return meta['resourceSets'][0]['resources'][0]['bbox']