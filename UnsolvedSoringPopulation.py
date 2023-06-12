# ----------- Project Files -----------
import Parasite
# ----------- Python Package -----------
import random
import numpy as np

# ----------- Consts ----------
MUTATION_INDIVIDUALS = 20
ELITE_PERCENTAGE = 0.10


class UnsolvedSoringPopulation:
    population: list
    fitnesses: list

    population_size: int
    max_generations: int
    sorting_list_size: int

    def __init__(self, data) -> None:
        self.population = []
        self.fitnesses = []
        self.create_population(data)
        self.population_size = len(self.population)
        self.max_generations = data.max_generations
        self.sorting_list_size = data.sorting_list_size
        return
    
    def create_population(self, data) -> None:
        for i in range(data.population_size):
            parasite = Parasite.Parasite(list_size = data.sorting_list_size)
            self.population.append(parasite)
            self.fitnesses.append(parasite.score)
        return

    def genetic_algorithm(self) -> None:
        for index, parasite in enumerate(self.population):
            self.fitnesses[index] = parasite.score

        # Select the best individuals for reproduction
        elite_size = int(self.population_size * ELITE_PERCENTAGE)
        elites = sorted(self.population, 
                        key=lambda parasite: parasite.score_test,
                        reverse=False)[:elite_size]
        
        # Generate new individuals by applying crossover and mutation operators
        offspring = []
        while len(offspring) < self.population_size - elite_size:            
            child_gen = list(range(self.sorting_list_size))
            random.shuffle(child_gen)
            child = Parasite.Parasite(unsorted_list = child_gen)
            offspring.append(child)
            
        # mutation
        mutation_indexes = random.sample(range(len(offspring)), k= MUTATION_INDIVIDUALS)
        for i, index in enumerate(mutation_indexes):         
            offspring[index].mutation()
        
        self.population = elites + offspring

        # Find the parasite with the highest fitness        
        best_parasite = sorted(self.population, 
                               key=lambda parasite: parasite.score_test,
                               reverse=False)[0]

        best_fitness = best_parasite.score
        # print_scores_grah(scores)   
        return best_parasite.unsorted_list , best_fitness

    def print_population(self) -> None:
        for i, parasite in enumerate(self.population):
            print(f"the {i} parasite -> {parasite.unsorted_list}, and his score {parasite.score}")
        return
    
    def get_parasites(self) -> list:
        elite_size = int(self.population_size * ELITE_PERCENTAGE)
        elite_parasites = sorted(self.population, key=lambda parasite: parasite.score, reverse=True)[:elite_size]
        
        random_parasites = []
        for i in range(elite_size):
            unsorted_random_list = list(range(self.sorting_list_size))
            random.shuffle(unsorted_random_list)
            unsorted_random_list = Parasite.Parasite(unsorted_list = unsorted_random_list)
            random_parasites.append(unsorted_random_list)

        return elite_parasites + random_parasites
    
    def print_parasites(self, parasites: list) -> None:
        for i, parasite in enumerate(parasites):
            print(f"the {i} parasite -> {parasite.unsorted_list}, and his score {parasite.score}")
        return
    
    def get_parasites_as_lists(self):
        temp_parasites = self.get_parasites()
        parasites_as_lists = []
        for parasite in temp_parasites:
            parasites_as_lists.append(parasite.unsorted_list)

        return parasites_as_lists