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
            parasite = Parasite.Parasite(data.sorting_list_size)
            self.population.append(parasite)
            self.fitnesses.append(parasite.score)
        return
        

    def genetic_algorithem(self) -> None:
        # score: float = 0
        # pop_size: int = 100
        # dimensions: int = ackley.dimensions
        # max_generations: int = 100

        # population: list = []
        # fitnesses: list = []

        # create population
        # for index in range(pop_size):
        #     first_node_coordinates = [random.uniform(ackley.bounds[0], ackley.bounds[1]) for i in range(dimensions)]
        #     individual = Individual.Individual(first_node_coordinates)
        #     individual.score = ackley.function(individual)
        #     population.append(individual)

        #create fitnesses
        # for parasite in population:
        #     fitnesses.append(parasite.score)

        scores = []

        #starting GA
        for generation_index in range(self.max_generations):
            for index, parasite in enumerate(self.population):
                self.fitnesses[index] = self.fitness(parasite)

            average_fitness = np.average(self.fitnesses)
            # gen_time = time.time()
            print(f"========================================= {generation_index}")
            print(f"Average for this gen is {average_fitness}")

            # Select the best individuals for reproduction
            elite_size = int(self.population_size * ELITE_PERCENTAGE)
            elites = sorted(self.population, 
                            key=lambda parasite: parasite.score, 
                            reverse = True)[:elite_size] 
            scores.append(np.average(self.fitnesses))
            # Generate new individuals by applying crossover and mutation operators
            offspring = []
            while len(offspring) < self.population_size - elite_size:            
                parent1 = random.choice(elites)
                parent2 = random.choice(elites)

                child_gen = []

                rand_a = random.randint(0, self.sorting_list_size)
                child_gen = [parent1.unsorted_list[i] if i < rand_a else parent2.unsorted_list[i] for i in range(self.sorting_list_size)]
                child = Parasite.Parasite(self.sorting_list_size)

                child.unsorted_list = child_gen
                child.score = ackley.function(individual)           
                offspring.append(child)
                
            # mutation
            mutation_indexes = random.sample(range(len(offspring)), k= MUTATION_INDIVIDUALS)
            for i, index in enumerate(mutation_indexes):         
                # print(f"befor coord {offspring[index].coordinates}")  
                for i, dim in enumerate(offspring[index].coordinates): 
                    offspring[index].coordinates[i] *= random.random()
                # print(f"after coord {offspring[index].coordinates}")  
            population = elites + offspring

        # Find the individual with the highest fitness
        best_individual = population[0]
        
        for individual in population:
            individual.score = ackley.function(individual) 
            if best_individual.score < individual.score:
                best_individual = individual

        best_fitness = best_individual.score
        # print_scores_grah(scores)   
        return best_individual.coordinates , best_fitness
