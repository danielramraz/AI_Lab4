# ----------- File For Genetic Algorithm -----------
import Data
import Niche
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
MUTATION_RATE = 3
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
        self.best_individual = None
        self.best_fitness = 0
        self.test_result = []
        self.niches = []

        for index in range(self.data.population_size):
            individual = SortingNetwork(self.data)
            self.population.append(individual)
        self.set_fitnesses()
        return

    def set_fitnesses(self):
        self.fitnesses = []
        for individual in self.population:
            self.fitnesses.append(individual.score_test)
        return

    def genetic_algorithm(self, generation_index):
        # ----------- Printing graphs for the report -----------
        # x1 = []
        # y1 = []
        # ax = plt.axes()
        # ax.set(xlim=(0, 100),
        #        ylim=(0, 10),
        #        xlabel='Generation number',
        #        ylabel='Genetic diversification distance')
        # ----------- Elitism -----------
        elites = self.get_sorting_networks()

        if generation_index % MUTATION_RATE == 0:
            population_copy = self.population
            self.population = elites
            self.fix_population_by_testing()
            for ind in population_copy:
                if ind not in self.population:
                    self.population.append(ind)

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
        gen_time = time.time()
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
        self.population = offspring + elites
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

        # ----------- Print Time Information -----------
        # print(f"The absolute time for this gen is {time.time() - gen_time} sec")
        # print(f"The ticks time for this gen is {int(time.perf_counter())}")

        # ----------- Best Solution -----------
        # Find the individual with the highest fitness
        if generation_index == 0:
            self.best_individual = self.population[0]

        for individual in self.population:
            # if self.best_individual.score > individual.score and self.best_individual.score_test < individual.score_test:
            if self.best_individual.score_test < individual.score_test:
                self.best_individual = individual
                print("best individual changed")

        self.best_fitness = self.best_individual.score_test
        print("Sorting Network best_fitness:",  self.best_fitness)
        # ax.plot(np.array(x1), np.array(y1))
        # plt.show()
        return

    def get_sorting_networks(self):
        # Select the best individuals for testing
        elite_size = int(self.data.population_size * ELITE_PERCENTAGE)
        elite_indices = sorted(range(len(self.population)), key=lambda i: self.fitnesses[i], reverse=False)[:elite_size]
        elites = [self.population[i] for i in elite_indices]

        return elites

    def fix_population_by_testing(self):
        # ------ בניית גן לפי bins -------
        # bad_comparators = [(comparator, i, j, k)
        #                    for i, ind in enumerate(self.population)
        #                    for j, phase in enumerate(ind.gen)
        #                    for k, comparator in enumerate(phase)
        #                    if comparator.score == 0]
        #
        # remove_from_population = []
        # while bad_comparators:
        #     item = bad_comparators[0]
        #     if random.random() < 0.2:
        #         remove_from_population.append(item)
        #     else:
        #         item_2 = self.find_other_comparator(bad_comparators, item)
        #         if item_2:
        #             self.population[item[1]].gen[item[2]][item[3]] = item_2[0]
        #             self.population[item_2[1]].gen[item_2[2]][item_2[3]] = item[0]
        #             bad_comparators.remove(item_2)
        #         else:
        #             remove_from_population.append(item)
        #     bad_comparators.remove(item)
        #
        # sorted_combined = sorted(remove_from_population, key=lambda x: x[3], reverse=True)
        # for item in sorted_combined:
        #     self.population[item[1]].comparisons.remove(item[0].value)
        #     self.population[item[1]].gen[item[2]].remove(item[0])
        for i, ind in enumerate(self.population):
            comparators_scores = [comparator.score for j, comparator in enumerate(ind.gen)]
            min_score = min(comparators_scores)
            bad_comparators = [(comparator, j) for j, comparator in enumerate(ind.gen) if comparator.score == min_score]
            mutations_iterations = random.randint(0, 4)
            while mutations_iterations > 0:
                item = random.sample(bad_comparators, k=1)[0]
                self.indirect_replacement(item, i)
                bad_comparators.remove(item)
                mutations_iterations -= 1

            # try to remove all comparators with score 0  -------------------------------------
            # print(f"the comparators_scores are: {comparators_scores}")
            # for j, score in enumerate(comparators_scores):
            #     if score == 0:
            #         self.remove_n_add_new_comp(ind, j)
            # ---------------------------------------------------------------------------------

        # remove_from_population = []
        # while bad_comparators:
        #     item = bad_comparators[0]
        #     if random.random() < 0.2:
        #         remove_from_population.append(item)
        #     else:
        #         item_2 = self.find_other_comparator(bad_comparators, item)
        #         if item_2:
        #             self.population[item[1]].gen[item[2]] = item_2[0].copy()
        #             self.population[item_2[1]].gen[item_2[2]] = item[0].copy()
        #             bad_comparators.remove(item_2)
        #         else:
        #             remove_from_population.append(item)
        #     bad_comparators.remove(item)
        #
        # sorted_combined = sorted(remove_from_population, key=lambda x: x[2], reverse=True)
        # for item in sorted_combined:
        #     self.population[item[1]].gen.remove(item[0])
        #     self.population[item[1]].comparisons_number = len(self.population[item[1]].gen)
        #
        # remove_from_population = []
        # mutations_iterations = random.randint(1, 4)
        # while mutations_iterations > 0:
        #     item = random.sample(bad_comparators, k=1)[0]
        #     self.indirect_replacement(item)
        #     remove_from_population.append(item)
        #     bad_comparators.remove(item)
        #     mutations_iterations -= 1

        # sorted_combined = sorted(remove_from_population, key=lambda x: x[2], reverse=True)
        # for item in sorted_combined:
        #     self.population[item[1]].gen.remove_compertor(item[0])

        return

    def remove_n_add_new_comp(self, ind: SortingNetwork, j: int)->None:
        ind.remove_comparator(ind.gen[j])
        numbers = range(self.data.sorting_list_size)
        values = tuple(random.sample(numbers, k=2))
        new_comparator = Comparator(values)
        ind.gen.append(new_comparator)
        ind.calc_score()
        return
    
    def indirect_replacement(self, item: SortingNetwork, ind_index):
        gen_size = len(self.population[ind_index].gen)
        self.population[ind_index].remove_comparator(item[0])

        # Creating a new random comparator
        numbers = [i for i in range(self.data.sorting_list_size)]
        values = random.sample(numbers, k=2)
        if values[0] > values[1]:
            values[0], values[1] = values[1], values[0]
        values = tuple(values)
        comparator = Comparator(values)

        # Inserting the new comparator in a random index in the sorting network
        index = random.randint(0, gen_size)
        self.population[ind_index].gen.insert(index, comparator)

        return

    def find_other_comparator(self, comparators, item):
        # ------ בניית גן לפי bins -------
        # for comp in comparators:
        #     if item[0].value != comp[0].value and\
        #             comp[0].value not in self.population[item[1]].comparisons and\
        #             item[0].value not in self.population[comp[1]].comparisons:
        #         return comp

        for comp in comparators:
            if item[0].value != comp[0].value and\
                    comp[0].value not in self.population[item[1]].gen and\
                    item[0].value not in self.population[comp[1]].gen:
                return comp
        return None

    def genetic_diversification_special(self):
        return 0


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


def crossover_operator(parent1: SortingNetwork, parent2: SortingNetwork, data: Data):
    # ------ בניית גן לפי bins -------
    # phases_num = int((len(parent1.gen) + len(parent2.gen)) / 2)
    # comparisons_num = int((len(parent1.comparisons) + len(parent2.comparisons)) / 2)
    # if data.sorting_list_size == 16:
    #     child_gen = SmartInit.smart_vector_16().copy()
    #     comparisons_num -= SmartInit.num_comparators_init_vector_16
    # elif data.sorting_list_size == 8:
    #     child_gen = SmartInit.smart_vector_8().copy()
    #     comparisons_num -= SmartInit.num_comparators_init_vector_8
    #
    # current_phases_num = len(child_gen)
    # for i in range(current_phases_num, phases_num):
    #     if random.random() < 0.5 and i < len(parent1.gen) and parent1.gen[i]:
    #         child_gen.append(parent1.gen[i].copy())
    #         comparisons_num -= len(parent1.gen[i])
    #     elif i < len(parent2.gen) and parent2.gen[i]:
    #         child_gen.append(parent2.gen[i].copy())
    #         comparisons_num -= len(parent2.gen[i])
    #
    # child = SortingNetwork(data, child_gen)

    comparisons_num = int((len(parent1.gen) + len(parent2.gen)) / 2)
    child_gen = SortingNetworkHandler.create_generate_bitonic_network(data.sorting_list_size)
    for i in range(len(child_gen), comparisons_num):
        if random.random() < 0.5 and i < len(parent1.gen) and parent1.gen[i]:
            child_gen.append(parent1.gen[i].copy())
        elif i < len(parent2.gen) and parent2.gen[i]:
            child_gen.append(parent2.gen[i].copy())

    child = SortingNetwork(data, child_gen)

    return child







