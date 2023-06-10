# ----------- Project Files -----------
from datetime import timedelta
import random

import Comparator
from Data import Data
from SortingNetworkPopulation import SortingNetworkPopulation
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
import SortingNetworkHandler
import TestsHub
import FinalTest
# ----------- Python Package -----------
import time
import random
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

            sorting_network_tests_results, parasites_tests_results = TestsHub.run_tests(sorting_networks, parasites)
            # if parasites_tests_results is None:
            #     self.sorting_networks.best_individual = sorting_network_tests_results
            #     break
            
            self.sorting_networks.tests_results = sorting_network_tests_results
            self.challengers.tests_results = parasites_tests_results

        # ----------- Print Time Information -----------
        total_time_sec = time.time() - gen_time
        total_time = timedelta(seconds=total_time_sec)
        print(f"The absolute time for this gen is {total_time} sec")
        print(f"The ticks time for this gen is {int(time.perf_counter())}")

        self.sorting_networks.set_best()
        # self.test_best_sorting_network()
        self.sorting_networks.best_individual.print_sorting_network()
        FinalTest.sorting_network_final_test(self.sorting_networks.best_individual, self.challengers)
        self.sorting_networks.best_individual.print_sorting_network()
        return

    def test_best_sorting_network(self) -> None:
        print("Depth: ", self.sorting_networks.best_individual.score)

        for i in range(10):
            unsorted_list = list(range(16))
            random.shuffle(unsorted_list)
            print(f"----- Test {i+1} -----")
            print("unsorted_list:", unsorted_list)
            for k, comparator in enumerate(self.sorting_networks.best_individual.gen):
                self.comper_n_swap(comparator, unsorted_list)
            print("sorted_list:", unsorted_list)

        return

    def print_solution_as_network(self) -> None:
        
        return

    def comper_n_swap(self, comperator: Comparator, lst: list) -> None:
        x = comperator.value[0]
        y = comperator.value[1]

        if lst[x] > lst[y]:
            temp = lst[x]
            lst[x] = lst[y]
            lst[y] = temp
            return
