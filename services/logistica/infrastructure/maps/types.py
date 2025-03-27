from typing import List


class Bounds:
    def __init__(self, northeast, southwest):
        self.northeast = northeast
        self.southwest = southwest

class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class Distance:
    def __init__(self, text, value):
        self.text = text
        self.value = value

class Duration:
    def __init__(self, text, value):
        self.text = text
        self.value = value

class Leg:
    def __init__(self, distance, duration, end_address, end_location, start_address, start_location):
        self.distance = distance
        self.duration = duration
        self.end_address = end_address
        self.end_location = end_location
        self.start_address = start_address
        self.start_location = start_location

class TypedObject:
    def __init__(self, bounds: List[Bounds], legs: List[Leg]):
        self.bounds = bounds
        self.legs = legs
