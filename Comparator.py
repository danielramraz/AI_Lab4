
class Comparator:
    score: float
    value: tuple

    def __init__(self, value):
        self.value = tuple(value)
        self.score = 0
