from typing import List


class Coordinate(object):
    def __init__(self, date: List[int], brand: str, name: List[str], type: str, color: List[str], images: List[str]):
        self.year = date[0]
        self.month = date[1]
        self.day = date[2]
        self.brand = brand
        self.name = name
        self.type = type
        self.color = color
        self.images = images
