# ----------- Project Files -----------

# ----------- Python Package -----------
import random
# ----------- Consts ----------


class Parasite:
    unsorted_list: list
    score: float

    def __init__(self, list_size = None, ) -> None:
        self.unsorted_list = range(list_size)
        random.shuffle(self.unsorted_list)
        self.score = self.fitness(self.unsorted_list)
        return

    def fitness(self, parasite) -> float:
        score = 0

        return score
    
    def 
