# ----------- File For Genetic Algorithm -----------
from Data import Data
# ----------- Python Package -----------
import numpy as np
import random
# ----------- Consts Parameters -----------
# ----------- Consts Name  -----------


class SortingNetwork:
    score: float
    score_test: float
    gen: list
    gen_len: int
    age: int

    def __init__(self, data: Data):
        self.gen = self.create_gen(data)
        self.score = self.calc_score(data)

    def create_gen(self, data):
        gen = []
        numbers = [i for i in range(data.sorting_list_size)]
        phase = []
        for i in range(data.size_vector):
            if numbers:
                compertor = random.sample(numbers, k=2)[0]
                numbers.remove(compertor[0])
                numbers.remove(compertor[1])
                phase.append(compertor)
            else:
                gen.append(phase)
                numbers = [i for i in range(data.sorting_list_size)]
                phase = []

        return gen

    def calc_score(self, data):
        numbers_in_gen = self.find_numbers_in_gen().to_array()
        var = np.var(numbers_in_gen)
        return var

    def find_numbers_in_gen(self):
        numbers_in_gen = []
        for i, item in enumerate(self.gen):
            item_list = sum(item, [])
            numbers_in_gen += item_list
        numbers_in_gen = sum(numbers_in_gen, [])

        return numbers_in_gen
