import random

class Food():
    def __init__(self, possible_spots):
        self.position = random.choice(possible_spots)