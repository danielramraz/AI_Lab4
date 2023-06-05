# ----------- File For Genetic Algorithm -----------
import Data
import SmartInit
from Comparator import Comparator
# ----------- Python Package -----------
import numpy as np
import random
# ----------- Consts Name  -----------
MAX_ATTEMPTS = 5


class SortingNetwork:
    score: float
    score_test: float
    score_share: float
    gen: list
    comparisons_number: int

    def __init__(self, data: Data, gen=None) -> None:
        self.comparisons_number = SmartInit.ideal_num_comparators_vector_16
        if gen is not None:
            self.gen = gen
        else:
            self.gen = self.create_gen(data)
        self.calc_score()
        self.score_test = 0
        self.score_share = 0

        return

    def create_gen(self, data: Data) -> list:
        numbers = [i for i in range(data.sorting_list_size)]
        gen = SmartInit.smart_vector_16().copy()

        while len(gen) < self.comparisons_number:
            values = random.sample(numbers, k=2)
            if values[0] > values[1]:
                values[0],  values[1] = values[1],  values[0]
            values = tuple(values)
            comparator = Comparator(values)
            gen.append(comparator)

        return gen

    def calc_score(self) -> None:
        numbers_in_gen = np.array(self.find_numbers_in_gen())
        freq = np.bincount(numbers_in_gen)
        self.score = np.max(freq)

        return

    def find_numbers_in_gen(self) -> list:
        numbers_in_gen = []
        for i, comper in enumerate(self.gen):
            numbers_in_gen.append(comper.value[0])
            numbers_in_gen.append(comper.value[1])

        return numbers_in_gen

    # distance = different comparators at the same index
    def distance_func(self, ind) -> float:
        self_comparators = [comp.value for comp in self.gen]
        ind_comparators = [comp.value for comp in ind.gen]
        self_comparators_set = set(self_comparators)
        ind_comparators_set = set(ind_comparators)
        dist = len(self_comparators_set.difference(ind_comparators_set))
        return dist

    # distance = different comparators at the same index between gen and population gens
    def genetic_diversification_distance(self, population: list) -> float:
        dist = 0
        self_comparators_set = set([comp.value for comp in self.gen])
        for ind in population:
            ind_comparators_set = set([comp.value for comp in ind.gen])
            dist += len(self_comparators_set.difference(ind_comparators_set))

        # Normalize the distance by the amount of population
        dist = dist / len(population)
        return dist

    def remove_comparator(self, comp_index: int) -> None:
        self.gen.remove(self.gen[comp_index])
        return
    
    def print_sorting_network(self) -> None:
        for i, comperator in enumerate(self.gen): 
            print(i, comperator.value, comperator.score)
                
        return


def create_generate_bitonic_network(sorting_list_size: int) -> list:
    comparisons = generate_bitonic_network(sorting_list_size)
    new_comparisons = []
    for i, comp in enumerate(comparisons):
        comparator = Comparator(comp)
        new_comparisons.append(comparator)

    return new_comparisons


def generate_bitonic_network(sorting_list_size: int) -> list:
    if sorting_list_size == 1:
        return []

    # Generate comparisons for the first half of the network
    comparisons = generate_bitonic_network(sorting_list_size//2)
    # Mirror the comparisons for the second half of the network
    comparisons += [(i + sorting_list_size // 2, j + sorting_list_size // 2) for i, j in comparisons[::-1]]

    # Add additional comparisons to create a bitonic sequence
    for i in range(sorting_list_size // 2):
        comparisons.append((i, i + sorting_list_size // 2))

    return comparisons


