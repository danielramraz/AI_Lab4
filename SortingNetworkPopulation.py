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
ELITE_PERCENTAGE = 0.30
MUTATION_RATE = 5
# ----------- Consts Name  -----------
NONE = 0
SINGLE = 1
TWO = 2
UNIFORM = 3


class SortingNetworkPopulation:
    data: Data
    population: list
    fitnesses: list
    best_individual: SortingNetwork
    best_fitness: float

    def __init__(self, data: Data):
        self.data = data
        self.population = []
        self.fitnesses = []
        self.fitnesses_test = []
        self.best_individual = None
        self.best_fitness = 0
        self.test_result = []
        self.niches = []

        for index in range(self.data.population_size):
            individual = SortingNetwork(self.data)
            self.population.append(individual)
        self.set_fitnesses()

        # ----------- Printing graphs for the report -----------
        self.x1 = []
        self.y1 = []
        self.ax = plt.axes()
        self.ax.set(xlim=(0, 200),
                    ylim=(0, 60000),
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
        if generation_index == 1:
            self.best_individual = self.population[0]

        for individual in self.population:
            if self.best_individual.score_test < individual.score_test:
                self.best_individual = individual.copy()
                print("best individual changed")
            elif self.best_individual.score_test == individual.score_test and self.best_individual.score > individual.score:
                self.best_individual = individual.copy()
                print("best individual changed + Depth")

        self.best_fitness = self.best_individual.score_test
        print("Sorting Network best_fitness:",  self.best_fitness)

        # -----------  Fix Sorting Network After Test -----------
        population_copy = self.population
        self.population = self.tests_results
        self.fix_population_by_testing()
        self.population = population_copy

        # ----------- Elitism -----------
        self.set_fitnesses()
        elites = self.get_elite_networks()
        self.population = elites

        # ----------- Update Population -----------
        # for ind in population_copy:
        #     if ind not in self.population:
        #         self.population.append(ind)

        # Select the best individuals for reproduction
        # elites = self.get_sorting_networks()
        # for ind in elites:
        #     self.population.remove(ind)

        # ----------- Clustering -----------
        # if generation_index % 10 == 0:
        #     self.niches = []
        #     clusters = Clustering.shared_fitness_cluster(self.population)
        #     for cluster in clusters:
        #         niche = Niche.Niche(cluster)
        #         self.niches.append(niche)

        # ----------- Print Fitness Information -----------
        # print(f"========================================= {generation_index}")
        # for index, niche in enumerate(self.niches):
        #     average, variance, sd = self.average_fitness(niche.fitnesses)
        #     print(f"Average for niche {index + 1} is {average}")
        #     print(f"Selection Pressure for niche {index + 1} is {variance}")
        #     x1.append(generation_index)
        #     y1.append(average)

        # ----------- Generate New Individuals -----------
        offspring = []
        while len(offspring) < self.data.population_size - len(elites):
            parent1 = random.choice(elites)
            parent2 = random.choice(elites)
            child = crossover_operator(parent1, parent2, self.data)
            offspring.append(child)
        # for niche in self.niches:
        #     niche.generate_individuals(self.data)

        # ----------- Update Population -----------
        self.population += offspring
        for ind in self.population:
            ind.calc_score()
        self.set_fitnesses()

        # self.population = []
        # for niche in self.niches:
        #     for ind in niche.individuals:
        #         self.population.append(ind)
        # self.set_fitnesses()

        # ----------- Genetic Diversification -----------
        # distance = 0
        # for ind in self.population:
        #     distance += ind.genetic_diversification_distance(self.population)
        # distance = distance / len(self.population)
        # special = self.genetic_diversification_special()
        # print(f"The genetic diversification distance is: {distance}")
        # print(f"The genetic diversification special is: {special}")

        # distance_all = 0
        # for index, niche in enumerate(self.niches):
        #     distance = 0
        #     for ind in niche.individuals:
        #         distance += ind.genetic_diversification_distance(niche.individuals)
        #     distance = distance / len(self.population)
        #     distance_all += distance
        #     print(f"The genetic diversification distance for niche {index + 1} is: {distance}")

        # ----------- Best Solution -----------
        # Find the individual with the highest fitness

        # ----------- Update Best Sorting Network -----------
        # if generation_index == 1:
        #     self.best_individual = self.population[0]
        #
        # for individual in self.population:
        #     if self.best_individual.score_test < individual.score_test:
        #         self.best_individual = individual.copy()
        #         print("best individual changed")
        #     elif self.best_individual.score_test == individual.score_test and self.best_individual.score > individual.score:
        #         self.best_individual = individual.copy()
        #         print("best individual changed + Depth")
        #
        # self.best_fitness = self.best_individual.score_test
        # print("Sorting Network best_fitness:",  self.best_fitness)

        self.x1.append(generation_index)
        self.y1.append(self.best_fitness)
        # if generation_index == self.data.max_generations-1:
        #     self.ax.plot(np.array(self.x1), np.array(self.y1))
        #     plt.show()
        return

    def get_elite_networks(self) -> list:
        # Select the best individuals for testing
        elite_size = int(self.data.population_size * ELITE_PERCENTAGE)
        elite_indices = sorted(range(len(self.population)), key=lambda i: self.fitnesses_test[i], reverse=True)[:elite_size]
        elites = [self.population[i].copy() for i in elite_indices]

        return elites

    def get_sorting_networks(self) -> list:
        # Select the best individuals for testing
        elite_size = int(self.data.population_size * ELITE_PERCENTAGE)
        # elite_indices = sorted(range(len(self.population)), key=lambda i: self.fitnesses[i], reverse=False)[:elite_size]
        # elites = [self.population[i] for i in elite_indices]

        sorting_networks_for_test = [ind for ind in self.population if ind.score >= 13]
        if len(sorting_networks_for_test) > elite_size:

            # ----------- Tournament Ranking -----------
            sorting_networks_for_test = random.sample(sorting_networks_for_test, k=elite_size)

            # ----------- Elite -----------
            # sorting_networks_for_test_fitnesses = []
            # for ind in sorting_networks_for_test:
            #     sorting_networks_for_test_fitnesses.append(ind.score_test)

            # elite_indices = sorted(range(len(sorting_networks_for_test)),
            #                        key=lambda i: sorting_networks_for_test_fitnesses[i],
            #                        reverse=True)[:elite_size]
            #
            # elites = [sorting_networks_for_test[i] for i in elite_indices]
            # sorting_networks_for_test = elites

        print("Size sorting_networks for test:", len(sorting_networks_for_test))
        return sorting_networks_for_test

    def fix_population_by_testing(self) -> None:
        for i, ind in enumerate(self.population):
            # min_score = min([comparator.score for j, comparator in enumerate(ind.gen)])
            bad_comparators_index = [j for j, comparator in enumerate(ind.gen)
                                     if comparator.score == 0 and j >= SmartInit.num_comparators_init_vector_16]
            bad_comparators_index.reverse()
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

    def genetic_diversification_special(self):
        return 0

    def set_best(self) -> None:
        self.population += self.tests_results
        for individual in self.population:
            if self.best_individual.score_test < individual.score_test:
                self.best_individual = individual
                self.best_fitness = self.best_individual.score_test
                print("best individual changed")

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
        if random.random() < 0.5 and i < len(parent1.gen) and parent1.gen[i]:
            child_gen.append(parent1.gen[i].copy())
        elif i < len(parent2.gen) and parent2.gen[i]:
            child_gen.append(parent2.gen[i].copy())

    child = SortingNetwork(data, child_gen)

    return child







