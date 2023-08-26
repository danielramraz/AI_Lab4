# ----------- File For Genetic Algorithm -----------
import Data
from Comparator import Comparator
from SortingNetworkHandler import SortingNetwork
# ----------- Python Package -----------
import numpy as np
import matplotlib.pyplot as plt
import random

# ----------- Consts Parameters -----------
ELITE_PERCENTAGE_ORIG = 0.30
MUTATION_PERCENTAGE = 0.30
# ----------- Consts Name  -----------


class SortingNetworkPopulation:
    data: Data
    population: list
    fitnesses: list
    fitnesses_test: list
    best_individual: SortingNetwork
    best_fitness: float
    ELITE_PERCENTAGE: float
    MUTATION_PERCENTAGE: float

    def __init__(self, data: Data):
        self.data = data
        self.population = []
        self.fitnesses = []
        self.fitnesses_test = []
        self.avg_fitnesses_test = []
        self.tests_results = []
        self.elites = []

        self.ELITE_PERCENTAGE = data.initial_unsolved_soring_network_elite_percentage
        self.MUTATION_PERCENTAGE = MUTATION_PERCENTAGE

        for index in range(self.data.population_size):
            individual = SortingNetwork(self.data)
            self.population.append(individual)

        self.set_fitnesses()
        self.best_individual = self.population[0]
        self.best_fitness = 0

        self.init_graph_parameters(data)
        return

    def set_fitnesses(self) -> None:
        self.fitnesses = []
        self.fitnesses_test = []

        for individual in self.population:
            self.fitnesses_test.append(individual.score_test)
            self.fitnesses.append(individual.score)
        return

    def genetic_algorithm(self, generation_index: int) -> None:
        # ----------- Update Best Sorting Network After Test -----------
        self.set_best_sorting_network()

        # ----------- Elitism -----------
        self.set_fitnesses()
        self.elites = self.get_elite_networks()

        # -----------  Fix Sorting Network After Test -----------
        self.population = self.tests_results
        last_generation: bool = generation_index == self.data.max_generations -1
        if not last_generation:
            if generation_index % 20 == 0:
                self.fix_population_by_testing(4)
            else:
                self.fix_population_by_testing(3)
        self.population += self.elites

        # ----------- Generate New Individuals -----------
        offspring = []
        while len(offspring) + len(self.population) < self.data.population_size:
            parent1 = random.choice(self.elites)
            parent2 = random.choice(self.elites)
            child = crossover_operator(parent1, parent2, self.data)
            offspring.append(child)

        # ----------- Update Population -----------
        self.population += offspring

        self.set_fitnesses()
        self.add_info_to_graph(generation_index, self.best_fitness, self.get_average_score())

        return

    def get_elite_networks(self) -> list:
        # Select the best individuals for evolution
        elite_size = int(self.data.population_size * self.ELITE_PERCENTAGE)
        elite_indices = sorted(range(len(self.population)), key=lambda i: self.fitnesses_test[i], reverse=True)[:elite_size]
        elites = [self.population[i].copy() for i in elite_indices]

        return elites

    def get_sorting_networks(self, generation_index: int) -> list:
        valid_size = int((self.data.population_size * self.ELITE_PERCENTAGE))
        sorting_networks_for_test_indices = sorted(range(len(self.population)), key=lambda i: self.fitnesses[i], reverse=False)[:valid_size]
        sorting_networks_for_test = [self.population[i] for i in sorting_networks_for_test_indices]

        return sorting_networks_for_test

    def get_sorting_networks_for_mutation(self, elites: list, generation_index: int) -> list:
        mutation_size = int(self.data.population_size * self.MUTATION_PERCENTAGE)
        sorting_networks_for_mutation = random.sample(self.population, k=mutation_size)
        return sorting_networks_for_mutation

    def fix_population_by_testing(self, comp_num: int) -> None:
        for i, ind in enumerate(self.population):
            comparators_scores = [comparator.score for j, comparator in enumerate(ind.gen)]
            bad_comparators_index = sorted(range(len(comparators_scores)), key=lambda i: comparators_scores[i], reverse=False)[:comp_num]
            bad_comparators_index.sort(reverse=True)
            self.remove_bad_comparators(ind, bad_comparators_index)
            self.indirect_replacement(ind, len(bad_comparators_index))
            ind.calc_score()

        return

    def remove_bad_comparators(self, ind: SortingNetwork, bad_comparators_index: list) -> None:
        for i, comp_index in enumerate(bad_comparators_index):
            ind.remove_comparator(comp_index)
        return

    def indirect_replacement(self, ind: SortingNetwork, num_new_comparators: int) -> None:
        numbers = range(self.data.sorting_list_size)
        while num_new_comparators > 0:
            gen_size = len(ind.gen)
            values = random.sample(numbers, k=2)
            if values[0] > values[1]:
                values[0], values[1] = values[1], values[0]

            new_comparator = Comparator(values)
            # Inserting the new comparator in a random index in the sorting network
            if self.data.sorting_list_size == 8:
                index = random.randint(0, gen_size)
            elif self.data.sorting_list_size == 16:
                index = random.randint(SmartInit.num_comparators_init_vector_16, gen_size)
            ind.gen.insert(index, new_comparator)
            num_new_comparators -= 1

        return

    def set_best_sorting_network(self) -> None:
        for individual in self.population:
            if self.best_individual.score_test < individual.score_test:
                self.best_individual = individual.copy()
                print("!!! Best individual changed !!!")
            elif self.best_individual.score_test == individual.score_test and self.best_individual.score > individual.score:
                self.best_individual = individual.copy()
                print("!!! Best individual changed + Depth !!!")

        self.best_fitness = self.best_individual.score_test
        print("Sorting Network best_fitness:", self.best_fitness)
        print("Depth:", self.best_individual.score)

        return

    def genetic_diversification_special(self):
        return 0

    def set_elite_percentage(self, perc: float) -> None:
        self.ELITE_PERCENTAGE = perc
        return
    
    def set_mutation_percentage(self, perc: float) -> None:
        self.MUTATION_PERCENTAGE = perc
        return
    
    def get_average_score(self) -> float:
        avg_score = 0
        score_test_count = 0
        for ind in self.population:
            if ind.score_test != 0:
                avg_score += ind.score_test
                score_test_count += 1
        if score_test_count == 0:
            return 0
        return avg_score / score_test_count

    def init_graph_parameters(self, data: Data) -> None:
        self.x1 = []
        self.y1 = []
        self.z1 = []
        self.ax = plt.axes()
        self.ax.set(xlabel='Generation number',
                    ylabel='Best Fitness')
        return
    
    def add_info_to_graph(self, generation_index, best_fitness, avg_fitness) -> None:
        self.x1.append(generation_index)
        self.y1.append(best_fitness)
        self.z1.append(avg_fitness)
        return
    
    def plot_score_graph(self) -> None:
        self.ax.plot(np.array(self.x1), np.array(self.y1), label = "best score")
        self.ax.plot(np.array(self.x1), np.array(self.z1), label = "average score")
        plt.legend()
        plt.show()
        return

#   ----------------- not class functions -----------------

def average_fitness(fitness: list):
    if not fitness:
        return 0
    try:
        average = sum(fitness) / len(fitness)
        variance = sum([((x - average) ** 2) for x in fitness]) / (len(fitness) - 1)
    except:
        average = 0
        variance = 0
    sd = variance ** 0.5
    return average, variance, sd


def crossover_operator(parent1: SortingNetwork, parent2: SortingNetwork, data: Data) -> SortingNetwork:
    comparisons_num = int((len(parent1.gen) + len(parent2.gen)) / 2)
    child_gen = []
    init_len_child_gen = len(child_gen)
    for i in range(init_len_child_gen, comparisons_num):
        if parent1.gen[i].score >= parent2.gen[i].score:
            child_gen.append(parent1.gen[i].copy())
        elif i < len(parent2.gen) and parent2.gen[i]:
            child_gen.append(parent2.gen[i].copy())

    child = SortingNetwork(data, child_gen)

    return child
