"""
Custom classes for web app
"""

class CarForMenu():
    """
    CarForManu class.
    """
    def __init__(self, photo_path, model, type, space_for_people, money) -> None:
        self.photo_path = photo_path
        self.model = model
        self.type = type
        self.space_for_people = space_for_people
        self.money = money
