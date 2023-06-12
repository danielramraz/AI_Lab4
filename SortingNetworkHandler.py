# ----------- File For Genetic Algorithm -----------
import Data
import SmartInit
from Comparator import Comparator
# ----------- Python Package -----------
import numpy as np
import random
import matplotlib.pyplot as plt
# ----------- Consts Name  -----------
MAX_ATTEMPTS = 5


class SortingNetwork:
    score: float
    score_test: float
    score_share: float
    gen: list
    comparisons_number: int

    def __init__(self, data: Data = None, gen: list = None, score_test: float = None) -> None:
        self.comparisons_number = SmartInit.ideal_num_comparators_vector_16
        if gen is not None:
            self.gen = gen
        else:
            self.gen = self.create_gen(data)
        self.calc_score()
        if score_test is not None:
            self.score_test = score_test
        else:
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

    def copy(self):
        new_gen = []
        for comperator in self.gen:
            new_comperator = comperator.copy()
            new_gen.append(new_comperator)

        new_sorting_network = SortingNetwork(gen=new_gen, score_test=self.score_test)
        return new_sorting_network

    def get_max_input(self):
        max_input = 0
        for comp in self.gen:
            max_input = max(max_input, max(comp.value))
        return max_input
    
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


def plot_sorting_network(sorting_network: SortingNetwork) -> None:
    # Extract the comparators from the sorting network
    comparators = [comp.value for comp in sorting_network.gen]

    # Create a graph using matplotlib
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    # Calculate the number of layers in the sorting network
    num_layers = max(max(pair) for pair in comparators)

    # Set the horizontal spacing between the comparators
    spacing = 1.0 / (num_layers + 2)

    # Plot the comparators
    for i, (x, y) in enumerate(comparators):
        # Calculate the x-coordinates of the comparators
        x_coords = [i * spacing, (i + 1) * spacing]

        # Calculate the y-coordinates of the comparators
        y_coords = [(num_layers - x) * spacing, (num_layers - y ) * spacing]

        # Plot the lines connecting the comparators
        ax.plot(x_coords, y_coords, 'k', linewidth=0.5)

        # Plot the circles representing the comparators
        ax.plot(x_coords, y_coords, 'ko', markersize=4)

    # Plot horizontal lines representing the index
    for i in range(num_layers + 1):
        ax.plot([0, len(comparators) * spacing], [i * spacing, i * spacing], 'k', linewidth=0.5, linestyle='--')

    # Show the plot
    plt.show()



def plot_sorting_network2(sorting_network: SortingNetwork) -> None:
    comparators = sorting_network.gen
    num_layers = sorting_network.get_max_input() + 1

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    spacing = 1.0 / (num_layers + 2)

    for comp in comparators:
        x_coord = comp.index * spacing

        y_coords = [(num_layers - comp.value[0] + 1) * spacing, (num_layers - comp.value[1] + 1) * spacing]

        ax.plot([x_coord, x_coord], y_coords, 'k', linewidth=1)
        ax.plot(x_coord, y_coords[0], 'ko', markersize=4)
        ax.plot(x_coord, y_coords[1], 'ko', markersize=4)

    for i in range(num_layers + 1):
        ax.plot([0, len(comparators) * spacing], [i * spacing, i * spacing], 'k', linewidth=0.5, linestyle='--')

    plt.show()
