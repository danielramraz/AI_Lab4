# ----------- Project Files -----------
import Parasite
# ----------- Python Package -----------
import random
import numpy as np

# ----------- Consts ----------
MUTATION_INDIVIDUALS = 20
ELITE_PERCENTAGE = 0.20


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

        # scores = []

        #starting GA
        for generation_index in range(self.max_generations):
            for index, parasite in enumerate(self.population):
                self.fitnesses[index] = parasite.score

            average_fitness = np.average(self.fitnesses)
            # gen_time = time.time()
            # print(f"========================================= {generation_index}")
            # print(f"Average for this gen is {average_fitness}")

            # Select the best individuals for reproduction
            elite_size = int(self.population_size * ELITE_PERCENTAGE)
            elites = sorted(self.population, 
                            key=lambda parasite: parasite.score, 
                            reverse = True)[:elite_size] 
            # scores.append(np.average(self.fitnesses))
            # Generate new individuals by applying crossover and mutation operators
            offspring = []
            while len(offspring) < self.population_size - elite_size:            
                # parent1 = random.choice(elites)
                # parent2 = random.choice(elites)
                # child_gen = self.cx(parent1, parent2)
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
                               key=lambda parasite: parasite.score, 
                               reverse = False)[-1]                 

        best_fitness = best_parasite.score
        # print_scores_grah(scores)   
        return best_parasite.unsorted_list , best_fitness

    def cx(self, parent1: Parasite, parent2: Parasite) -> list:
        p1 = parent1.unsorted_list
        p2 = parent2.unsorted_list

        cycles = [-1] * len(p1)
        cycle_no = 1
        cycle_start = (i for i, v in enumerate(cycles) if v < 0)

        for pos in cycle_start:

            while cycles[pos] < 0:
                cycles[pos] = cycle_no
                if p2[pos] in p1:
                    pos = p1.index(p2[pos])
                else:
                    pos = 0
            cycle_no += 1

        child_gen = [p1[i] if n % 2 else p2[i] for i, n in enumerate(cycles)]
        # [print(f"sol-> {ind.index}->") for ind in child_gen]

        return child_gen

    def print_population(self) -> None:
        for i, parasite in enumerate(self.population):
            print(f"the {i} parasite -> {parasite.unsorted_list}, and his score {parasite.score}")
        return
    
    def get_parasites(self) -> list:
        elite_size = int(self.population_size * ELITE_PERCENTAGE)
        elite_parasites = sorted(self.population, 
                            key=lambda parasite: parasite.score, 
                            reverse = True)[:elite_size]
        
        # self.print_parasites(elite_parasites)
        return elite_parasites
    
    def print_parasites(self, parasites: list) -> None:
        for i, parasite in enumerate(parasites):
            print(f"the {i} parasite -> {parasite.unsorted_list}, and his score {parasite.score}")
        return