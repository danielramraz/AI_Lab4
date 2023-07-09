# ----------- File For Genetic Algorithm -----------
import Data
import Niche
import SmartInit
from Comparator import Comparator
from SortingNetworkHandler import SortingNetwork
import SortingNetworkHandler
import Clustering
# ----------- Python Package -----------
import time
import numpy as np
import matplotlib.pyplot as plt
import random
import math
# ----------- Consts Parameters -----------
MUTATION_PERCENTAGE = 0.30
# ----------- Consts Name  -----------
NONE = 0
SINGLE = 1
TWO = 2
UNIFORM = 3


class SortingNetworkPopulation:
    data: Data
    population: list
    fitnesses: list
    fitnesses_test: list
    best_individual: SortingNetwork
    best_fitness: float

    ELITE_PERCENTAGE: float
    
    def __init__(self, data: Data):
        self.data = data
        self.population = []
        self.fitnesses = []
        self.fitnesses_test = []
        self.test_result = []
        self.niches = []
        self.ELITE_PERCENTAGE = data.initial_unsolved_soring_network_elite_percentage

        for index in range(self.data.population_size):
            individual = SortingNetwork(self.data)
            self.population.append(individual)

        self.set_fitnesses()
        self.best_individual = self.population[0]
        self.best_fitness = 0

        # ----------- Printing graphs for the report -----------
        self.x1 = []
        self.y1 = []
        self.ax = plt.axes()
        self.ax.set(xlim=(0, self.data.max_generations),
                    ylim=(0, 16),
                    xlabel='Generation number',
                    ylabel='Best Fitness')
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
        self.set_fitnesses()
        self.set_best_sorting_networks()

        # ----------- Elitism -----------
        elites = self.get_elite_networks()

        # -----------  Fix Sorting Network After Test -----------
        self.population = self.get_sorting_networks_for_mutation()
        self.mutation_population()
        self.population += elites

        # ----------- Generate New Individuals -----------
        offspring = []
        while len(offspring) + len(self.population) < self.data.population_size:
            parent1 = random.choice(elites)
            parent2 = random.choice(elites)
            child = crossover_operator(parent1, parent2, self.data)
            offspring.append(child)

        # ----------- Update Population -----------
        self.population += offspring
        for ind in self.population:
            ind.calc_score()

        self.x1.append(generation_index)
        self.y1.append(self.best_fitness)
        if generation_index == self.data.max_generations-1:
            self.ax.plot(np.array(self.x1), np.array(self.y1))
            plt.show()
        return

    def get_elite_networks(self) -> list:
        # Select the best individuals for evolution
        elite_size = int(self.data.population_size * self.ELITE_PERCENTAGE)
        elite_indices = sorted(range(len(self.population)), key=lambda i: self.fitnesses_test[i], reverse=True)[:elite_size]
        elites = [self.population[i].copy() for i in elite_indices]

        return elites

    def get_sorting_networks(self, generation_index: int) -> list:
        elite_size = int((self.data.population_size * self.ELITE_PERCENTAGE) / 2)
        elite_indices = sorted(range(len(self.population)), key=lambda i: self.fitnesses_test[i], reverse=True)[:elite_size]
        elites = [self.population[i] for i in elite_indices]

        # Select individuals for testing with valid depth
        random_size = int((self.data.population_size * self.ELITE_PERCENTAGE) / 2)
        sorting_networks_valid_depth = [ind for ind in self.population if ind.score >= 13]
        if len(sorting_networks_valid_depth) > random_size:
            sorting_networks_valid_depth = random.sample(sorting_networks_valid_depth, k=random_size)

        sorting_networks_for_test = sorting_networks_valid_depth + elites + [self.best_individual]
        # if generation_index > 0:
        #     best_individual_after_mutation = self.best_individual.copy()
        #     self.mutation_for_sorting_network(best_individual_after_mutation)
        #     sorting_networks_for_test += [best_individual_after_mutation]

        return sorting_networks_for_test

    def get_sorting_networks_for_mutation(self) -> list:
        mutation_size = int(self.data.population_size * MUTATION_PERCENTAGE)

        # best_in_pop = False
        #
        # if self.best_individual in self.population:
        #     best_in_pop = True
        #     self.population.remove(self.best_individual)

        sorting_networks_for_mutation = random.sample(self.population, k=mutation_size)

        # if best_in_pop:
        #     self.population.append(self.best_individual)

        return sorting_networks_for_mutation

    def mutation_population(self) -> None:
        for i, ind in enumerate(self.population):
            self.mutation_for_sorting_network(ind)
            # min_score = min([comparator.score for j, comparator in enumerate(ind.gen)])
            # # bad_comparators_index = [j for j, comparator in enumerate(ind.gen)
            # #                          if comparator.score == min_score and
            # #                          j >= SmartInit.num_comparators_init_vector_16]
            #
            # bad_comparators_index = [j for j, comparator in enumerate(ind.gen)
            #                          if comparator.score == min_score]
            #
            # if len(bad_comparators_index) > 3:
            #     bad_comparators_index = random.sample(bad_comparators_index, k=3)
            #
            # bad_comparators_index.sort(reverse=True)
            # self.remove_bad_comparators(ind, bad_comparators_index)
            # self.indirect_replacement(ind, len(bad_comparators_index))
        return

    def mutation_for_sorting_network(self, ind: SortingNetwork):
        min_score = min([comparator.score for j, comparator in enumerate(ind.gen)])
        bad_comparators_index = [j for j, comparator in enumerate(ind.gen)
                                 if comparator.score == min_score]

        if len(bad_comparators_index) > 3:
            bad_comparators_index = random.sample(bad_comparators_index, k=3)

        bad_comparators_index.sort(reverse=True)
        self.remove_bad_comparators(ind, bad_comparators_index)
        self.indirect_replacement(ind, len(bad_comparators_index))
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
            index = random.randint(SmartInit.num_comparators_init_vector_16, gen_size)
            ind.gen.insert(index, new_comparator)
            num_new_comparators -= 1

        ind.calc_score()
        return

    def set_best_sorting_networks(self) -> None:
        for individual in self.population:
            if self.best_individual.score_test < individual.score_test:
                self.best_individual = individual
                print("!!! Best individual changed !!!")
            elif self.best_individual.score_test == individual.score_test and self.best_individual.score > individual.score:
                self.best_individual = individual
                print("!!! Best individual changed + Depth !!!")

        self.best_fitness = self.best_individual.score_test
        print("Sorting Network best_fitness:", self.best_fitness)

        return

    def genetic_diversification_special(self):
        return 0
    
    def set_elite_percentage(self, perc: float) -> None:
        self.ELITE_PERCENTAGE = perc
        return


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
    child_gen = SmartInit.smart_vector_16().copy()
    init_len_child_gen = len(child_gen)
    for i in range(init_len_child_gen, comparisons_num):
        if parent1.gen[i].score >= parent2.gen[i].score:
            child_gen.append(parent1.gen[i].copy())
        else:
            child_gen.append(parent2.gen[i].copy())
        # if random.random() < 0.5 and i < len(parent1.gen) and parent1.gen[i]:
        #     child_gen.append(parent1.gen[i].copy())
        # elif i < len(parent2.gen) and parent2.gen[i]:
        #     child_gen.append(parent2.gen[i].copy())

    child = SortingNetwork(data, child_gen)

    return child







