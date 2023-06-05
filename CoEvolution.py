# ----------- Project Files -----------
import random

from Data import Data
from SortingNetworkPopulation import SortingNetworkPopulation
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
import SortingNetworkHandler
import TestsHub
# ----------- Python Package -----------
import time
import threading
import numpy as np
# ----------- Consts ----------
setting_vector = [16]


class CoEvolution:
    data: Data
    sorting_networks: SortingNetworkPopulation
    challengers: UnsolvedSoringPopulation
    solution: SortingNetworkHandler

    def __init__(self) -> None:
        self.data = Data(setting_vector)
        self.challengers = UnsolvedSoringPopulation(self.data)
        self.sorting_networks = SortingNetworkPopulation(self.data)
        
        return

    def solve_sorting_network_problem(self) -> None:
        gen_time = time.time()

        for generation_index in range(self.data.max_generations):
            print(f"================================= generation_index ========= {generation_index}")

            parasites = self.challengers.get_parasites()
            sorting_networks = self.sorting_networks.get_sorting_networks()

            if generation_index != 0:
                self.sorting_networks.genetic_algorithm(generation_index)
                self.challengers.genetic_algorithm()


            sorting_network_tests_results, parasites_tests_results = TestsHub.run_tests(sorting_networks, 
                                                                                        parasites)
            
            self.sorting_networks.tests_results = sorting_network_tests_results
            self.challengers.tests_results = parasites_tests_results

        self.sorting_networks.set_best()
        print("Depth: ", self.sorting_networks.best_individual.score)
        unsorted_list = list(range(16))
        random.shuffle(unsorted_list)
        print("---------------------------")
        print("unsorted_list:", unsorted_list)
        for k, comperator in enumerate(self.sorting_networks.best_individual.gen):
            TestsHub.comper_n_swap(comperator, unsorted_list)
        print("sorted_list:", unsorted_list)

        # ----------- Print Time Information -----------
        # print(f"The absolute time for this gen is {time.time() - gen_time} sec")
        # print(f"The ticks time for this gen is {int(time.perf_counter())}")

        self.sorting_networks.best_individual.print_sorting_network()

        return
    
    def print_solution_as_network(self) -> None:
        
        return
