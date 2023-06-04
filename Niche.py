# ----------- File Form Lab -----------
import random
import Data
from SortingNetworkHandler import SortingNetwork
import SortingNetworkHandler
# ----------- Python Package -----------
import numpy as np
# ----------- Consts Name  -----------
SIGMA_SHARE = 20
ELITE_PERCENTAGE = 0.50

class Niche:
    sigma_share: float
    individuals: list
    fitnesses: list

    def __init__(self, individuals: list):
        self.sigma_share = 2
        self.Alpha = 1
        self.individuals = individuals
        self.similarity_matrix = self.init_matrix()
        self.update_score_share()
        self.fitnesses = [ind.score_test for ind in self.individuals]

    def init_matrix(self):
        niche_size = len(self.individuals)
        matrix = np.zeros((niche_size, niche_size))
        for i in range(niche_size):
            for j in range(niche_size):
                matrix[i][j] = self.individuals[i].distance_func(self.individuals[j])

        return matrix

    def update_score_share(self):
        for ind in self.individuals:
            share_score = []
            index_ind = self.individuals.index(ind)
            for j in range(len(self.individuals)):
                dist = self.similarity_matrix[index_ind][j]
                if dist < self.sigma_share:
                    share_score_j = 1 - ((dist/self.sigma_share) ** self.Alpha)
                    share_score.append(share_score_j)
            ind.score_share = ind.score / sum(share_score)
        return

    def generate_individuals(self, data: Data):

        niche_size = len(self.individuals)
        offspring = []
        parents_next_generation = []

        while len(offspring) + len(parents_next_generation) < niche_size:
            parent1 = random.choice(self.individuals)
            parent2 = random.choice(self.individuals)
            parents_next_generation.append(parent1)
            parents_next_generation.append(parent2)
            child = crossover_operator(parent1, parent2, data)
            offspring.append(child)

        self.individuals = offspring + parents_next_generation
        # while len(self.individuals) > niche_size:
        #     self.remove_worst_ind()

        return

    def get_elite(self):
        if len(self.individuals) == 1:
            return self.individuals

        # Select the best individuals for testing
        elite_size = int(len(self.individuals) * ELITE_PERCENTAGE)
        elite_indices = sorted(range(len(self.individuals)), key=lambda i: self.fitnesses[i], reverse=False)[:elite_size]
        elites = [self.individuals[i] for i in elite_indices]

        return elites

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

    def remove_worst_ind(self):
        worst_score = float('inf')
        for ind in self.individuals:
            if ind.score < worst_score:
                worst_score = ind.score
                worst_individual = ind

        self.individuals.remove(worst_individual)
        return


def crossover_operator(parent1: SortingNetwork, parent2: SortingNetwork, data: Data):
    comparisons_num = int((len(parent1.gen) + len(parent2.gen)) / 2)
    child_gen = SortingNetworkHandler.create_generate_bitonic_network(data.sorting_list_size)

    for i in range(len(child_gen), comparisons_num):
        if random.random() < 0.5 and i < len(parent1.gen) and parent1.gen[i]:
            child_gen.append(parent1.gen[i].copy())

        elif i < len(parent2.gen) and parent2.gen[i]:
            child_gen.append(parent2.gen[i].copy())

    child = SortingNetwork(data, child_gen)

    return child

