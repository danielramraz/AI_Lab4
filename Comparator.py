
class Comparator:
    score: float
    value: tuple
    index: int

    def __init__(self, value):
        self.value = tuple(value)
        self.score = 0

    def copy(self):
        new_comparator = Comparator(self.value)
        return new_comparator
