
class Comparator:
    score: float
    value: tuple

    def __init__(self, value):
        self.value = tuple(value)
        self.score = 0

    def copy(self):
        new_comparator = Comparator(self.value)
        new_comparator.score = self.score
        return new_comparator
