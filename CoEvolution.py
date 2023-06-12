# ----------- Project Files -----------
from Data import Data
from SortingNetworkPopulation import SortingNetworkPopulation
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
import SortingNetworkHandler
import TestsHub
import FinalTest
import SVG_SortingNetwork
# ----------- Python Package -----------
import time
import cProfile
from datetime import timedelta
import pstats
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
        profile = cProfile.Profile()
        profile.enable()

        for generation_index in range(self.data.max_generations):

            print(f"================================= generation_index ========= {generation_index}")

            parasites = self.challengers.get_parasites()
            sorting_networks = self.sorting_networks.get_sorting_networks()

            if generation_index != 0:
                self.sorting_networks.genetic_algorithm(generation_index)
                self.challengers.genetic_algorithm()

            sorting_network_tests_results, parasites_tests_results = TestsHub.run_tests(sorting_networks, parasites)
            
            self.sorting_networks.tests_results = sorting_network_tests_results
            self.challengers.tests_results = parasites_tests_results


        self.sorting_networks.set_best()
        self.sorting_networks.best_individual.console_print_sorting_network()
        FinalTest.sorting_network_final_test(self.sorting_networks.best_individual, self.challengers)
        self.sorting_networks.best_individual.console_print_sorting_network()
        

        # ----------- Print Time and Comput Information -----------

        total_time_sec = int(time.time() - gen_time)
        total_time = timedelta(seconds=total_time_sec)
        print(f"The absolute time for this gen is {total_time} sec")
        print(f"The ticks time for this gen is {int(time.perf_counter())}")

        profile.disable()
        ps = pstats.Stats(profile)
        ps.sort_stats('cumtime') 
        ps.print_stats(10)

        return

    def print_solution_as_network(self) -> None:
        SVG_SortingNetwork.SVG_print_sorting_network(self.sorting_networks.best_individual)
        return