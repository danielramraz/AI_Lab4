# ----------- Project Files -----------
import Data
import SmartInit
from Comparator import Comparator
# ----------- Python Package -----------
import numpy as np
import random
# ----------- Consts Parameters -----------
# ----------- Consts Name  -----------
MAX_ATTEMPTS = 5


class SortingNetwork:
    score: float
    score_test: float
    gen: list
    comparisons_number: int
    comparisons: list

    def __init__(self, data: Data, gen=None):
        if gen is not None:
            self.gen = gen
            self.comparisons = self.find_comparisons()
        else:
            self.gen,  self.comparisons = self.create_gen(data)
        self.comparisons_number = len(self.comparisons)
        self.calc_score()
        self.score_test = 0

        return

    def create_gen(self, data):
        comparisons = self.generate_bitonic_network(data.sorting_list_size)
        if data.sorting_list_size == 16:
            gen = SmartInit.smart_vector_16().copy()
        elif data.sorting_list_size == 8:
            gen = SmartInit.smart_vector_8().copy()

        comparators_num = data.sorting_list_size * np.log2(data.sorting_list_size)
        current_comparators_num_in_gen = data.num_comparators_init_vector

        while current_comparators_num_in_gen < comparators_num:
            # Defining the optional indexes for comparison
            numbers = [i for i in range(data.sorting_list_size)]
            comparators_in_phase = [i for i in range(1, int(data.sorting_list_size/2)+1)]

            # Setting the number of comparators in a phase
            # so that no more comparators are created than the final number of comparators
            attempts = 0
            while True:
                num_comparators_in_phase = random.sample(comparators_in_phase, k=1)[0]
                if current_comparators_num_in_gen + num_comparators_in_phase <= comparators_num:
                    break
                comparators_in_phase.remove(num_comparators_in_phase)

            # Initialize phase
            phase = []
            while num_comparators_in_phase > 0:
                attempts = 0
                # Random select indexes for comparison
                while attempts < MAX_ATTEMPTS:
                    values = random.sample(numbers, k=2)
                    if values[0] > values[1]:
                        values[0],  values[1] = values[1],  values[0]
                    values = tuple(values)
                    # Checking if there is an identical comparator
                    if values not in comparisons:
                        break
                    attempts += 1

                    # Checking if there are 2 numbers left in the list of index options
                    # and there is a comparator with these indexes - Then we will finish the phase
                    # pair = (numbers[0], numbers[1])
                    # if len(numbers) == 2 and pair in comparisons:
                    #     num_comparators_in_phase = 0
                    #     break

                if attempts == MAX_ATTEMPTS:
                    num_comparators_in_phase = 0

                # If  we haven't finished the phase -
                # Add the comparator to the phase and remove its indexes from the optional list of indexes
                if num_comparators_in_phase != 0:
                    comparisons.append(values)
                    comparator = Comparator(values)
                    numbers.remove(values[0])
                    numbers.remove(values[1])
                    phase.append(comparator)
                    num_comparators_in_phase -= 1
                    current_comparators_num_in_gen += 1

            # Add the phase to the sorting network
            gen.append(phase)

        return gen, comparisons

    def generate_bitonic_network(self, sorting_list_size):
        if sorting_list_size == 1:
            return []

        # Generate comparisons for the first half of the network
        comparisons = self.generate_bitonic_network(sorting_list_size//2)
        # Mirror the comparisons for the second half of the network
        comparisons += [(i + sorting_list_size // 2, j + sorting_list_size // 2) for i, j in comparisons[::-1]]

        # Add additional comparisons to create a bitonic sequence
        for i in range(sorting_list_size // 2):
            comparisons.append((i, i + sorting_list_size // 2))

        return comparisons

    def calc_score(self):
        numbers_in_gen = np.array(self.find_numbers_in_gen())
        # var = np.var(numbers_in_gen)
        # self.score = var
        freq = np.bincount(numbers_in_gen)
        self.score = np.max(freq)
        return

    def find_numbers_in_gen(self):
        numbers_in_gen = []
        for i, phase in enumerate(self.gen):
            for j, comper in enumerate(phase):
                numbers_in_gen.append(comper.value[0])
                numbers_in_gen.append(comper.value[1])

        return numbers_in_gen

    def calc_comparisons(self):
        comparisons = sum([len(item) for i, item in enumerate(self.gen)])
        return comparisons

    def genetic_diversification_distance(self, population):
        return 0

    def find_comparisons(self):
        comparisons = []
        for i, phase in enumerate(self.gen):
            for j, comparator in enumerate(phase):
                item = (comparator.value[0], comparator.value[1])
                comparisons.append(item)
        return comparisons



