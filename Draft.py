def genetic_algorithm(self, generation_index: int) -> None:
    # ----------- Update Best Sorting Network After Test -----------
    old_best_individual = self.best_individual
    self.set_best_sorting_network()

    # ----------- Elitism -----------
    self.set_fitnesses()
    elites = self.get_elite_networks()

    # -----------  Fix Sorting Network After Test -----------
    # if generation_index < 175:
    self.population = self.get_sorting_networks_for_mutation(elites, generation_index)
    self.fix_population_by_testing()
    self.population += elites
    # else:
    #     self.population = elites

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
    while len(offspring) + len(self.population) < self.data.population_size:
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

    self.x1.append(generation_index)
    self.y1.append(self.best_fitness)
    if generation_index == self.data.max_generations - 1:
        self.ax.plot(np.array(self.x1), np.array(self.y1))
        plt.show()
    return