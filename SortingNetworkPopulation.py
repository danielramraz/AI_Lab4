# ----------- File For Genetic Algorithm -----------
from Data import Data
import ParentOperator
import CrossoverOperator
# ----------- Python Package -----------
import time
import numpy as np
import matplotlib.pyplot as plt
import random

import math
# ----------- Consts Parameters -----------
MUTATION_INDIVIDUALS = 20
ELITE_PERCENTAGE = 0.20
# ----------- Consts Name  -----------
NONE = 0
SINGLE = 1
TWO = 2
UNIFORM = 3


class SortingNetworkPopulation:
    data: Data
    population: list
    best_fitness: float
    fitnesses: list

    def __init__(self, setting_vector=None):
        self.data = Data(setting_vector)
        self.population = []
        self.fitnesses = []
        self.best_individual = None
        self.best_fitness = 0
        self.test_result = []

        for index in range(self.data.pop_size):
            individual = Individual(self.data)
            self.population.append(individual)
        self.set_fitnesses()
        return

    def set_fitnesses(self):
        self.fitnesses = []
        for individual in self.population:
            self.fitnesses.append(individual.score)
        return

    def genetic_algorithm(self, migration=None, thread_index=None):
        # ----------- Printing graphs for the report -----------
        # x1 = []
        # y1 = []
        # ax = plt.axes()
        # ax.set(xlim=(0, 100),
        #        ylim=(0, 10),
        #        xlabel='Generation number',
        #        ylabel='Genetic diversification distance')

        for generation_index in range(self.data.max_generations):

            # ----------- Elitism -----------
            # Select the best individuals for reproduction
            elite_size = int(self.data.pop_size * ELITE_PERCENTAGE)
            elite_indices = sorted(range(self.data.pop_size), key=lambda i: self.fitnesses[i], reverse=True)[
                            :elite_size]
            elites = [self.population[i] for i in elite_indices]


            # ----------- Print Fitness Information -----------
            gen_time = time.time()
            print(f"======== {generation_index} ========")
            average, variance, sd = self.average_fitness(self.fitnesses)
            # self.show_histogram(self.fitnesses)
            # x1.append(generation_index)
            # y1.append(average)

            # ----------- Generate New Individuals -----------
            offspring = []
            while len(offspring) < self.data.pop_size - elite_size:
                parent1 = random.choice(elites)
                parent2 = random.choice(elites)

                child = crossover_operator(data.cross_operator, parent1, parent2, data.size_vector)
                offspring.append(child)

                if len(offspring) % 5 == 0:
                    child = mutation(child)
                    mutation_individuals -= 1

            # ----------- Update Population -----------
            self.population = elites
            for niche in self.niches:
                for ind in niche.individuals:
                    self.population.append(ind)

            # ----------- Update Population -----------
            # Update the age of each individual, if reached max_age - remove from population
            for individual in self.population:
                individual.age += 1
                individual.update_score(self.data)
                if individual.age == self.data.max_age:
                    self.population.remove(individual)

            # Update the size of the  population
            self.data.pop_size = len(self.population)

            # Update fitness list for population
            self.set_fitnesses()

            # ----------- Genetic Diversification -----------
            distance_all = 0
            for index, niche in enumerate(self.niches):
                distance = 0
                for ind in niche.individuals:
                    distance += ind.genetic_diversification_distance(niche.individuals)
                distance = distance / len(self.population)
                distance_all += distance
                special = niche.individuals[0].genetic_diversification_special(niche.individuals)
                print(f"The genetic diversification distance for niche {index + 1} is: {distance}")
                print(f"The genetic diversification special for niche {index + 1} is: {special}")
            # y1.append(distance_all/ len(self.niches))

            # ----------- Print Time Information -----------
            print(f"The absolute time for this gen is {time.time() - gen_time} sec")
            print(f"The ticks time for this gen is {int(time.perf_counter())}")

        # ----------- Best Solution -----------
        # Find the individual with the highest fitness
        self.best_individual = self.population[0]
        for individual in self.population:
            individual.update_score(self.data)
            if self.best_individual.score < individual.score:
                self.best_individual = individual

        self.best_fitness = self.best_individual.score
        # ax.plot(np.array(x1), np.array(y1))
        # plt.show()
        return

    def average_fitness(self, fitness: list):
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

    def show_histogram(self, array):
        np_array = np.array(array)
        plt.hist(np_array)
        plt.show()
        return


class Individual:
    score: float
    score_test: float
    gen_len: int
    age: int

    def __init__(self, data: Data):
        self.gen, self.numbers_in_gen = self.create_gen(data)
        self.score = self.calc_score(data)

    def create_gen(self, data):
        gen = []
        numbers_in_gen = []
        numbers = [i for i in range(data.size_vector)]
        phase = []
        for i in range(data.size_vector):
            if numbers:
                compertor = random.sample(numbers, k=2)[0]
                numbers_in_gen.append(compertor[0])
                numbers_in_gen.append(compertor[1])
                numbers.remove(compertor[0])
                numbers.remove(compertor[1])
                phase.append(compertor)
            else:
                gen.append(phase)
                numbers = [i for i in range(data.size_vector)]
                phase = []


        return

    def calc_score(self, data):
        score = 0
        sum_cols = np.sum(self.gen, axis=0)
        bad_value = [-5 for i, item in enumerate(sum_cols) if item > 5]
        good_value = [10 for i, item in enumerate(sum_cols) if item < 4]
        score = sum(bad_value) + sum(good_value)
        return score


def crossover_operator(parent1: Individual, parent2: Individual, num_genes: int):

    if operator == NONE:
        child_gen = [parent1.gen[i] if random.random() < 0.5 else parent2.gen[i] for i in range(num_genes)]

    if operator == SINGLE:
        rand_a = random.randint(0, num_genes)
        child_gen = [parent1.gen[i] if i < rand_a else parent2.gen[i] for i in range(num_genes)]

    elif operator == TWO:
        rand_a = random.randint(0, num_genes - 1)
        rand_b = random.randint(rand_a, num_genes)
        child_gen = [parent1.gen[i] if i < rand_a or i > rand_b else parent2.gen[i] for i in range(num_genes)]

    elif operator == UNIFORM:
        child_gen = [parent1.gen[i] if random.choice([0, 1]) else parent2.gen[i] for i in range(num_genes)]


    return child_gen






