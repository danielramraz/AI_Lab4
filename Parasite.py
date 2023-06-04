# ----------- Project Files -----------

# ----------- Python Package -----------
import random
# ----------- Consts ----------


class Parasite:
    unsorted_list: list
    score: float
    score_test: float

    def __init__(self, list_size = None, unsorted_list: list = None) -> None:
        if unsorted_list == None:
            self.unsorted_list = list(range(list_size))
            random.shuffle(self.unsorted_list)
        elif list_size == None:
            self.unsorted_list = unsorted_list

        self.score = self.fitness(self.unsorted_list)
        return

    def fitness(self, parasite) -> float:
        ''' the lowest score is the must suffled
        the highest score is sum of i^2 , 
        that is sorted list or almost sorted list'''

        score = 0
        for index, value in enumerate(parasite):
            score -= index * value

        return score
    
    def mutation(self) -> None:
        random.shuffle(self.unsorted_list)
        self.score = self.fitness(self.unsorted_list)
        return

    def copy(self):
        new_unsorted_list = self.unsorted_list.copy()
        new_parasite = Parasite(unsorted_list=new_unsorted_list)
        return new_parasite

    