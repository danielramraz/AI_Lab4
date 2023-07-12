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
import random
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
        sol_time = time.time()
        # end_count = 10

        for generation_index in range(self.data.max_generations):
            gen_time = time.time()
            # profile = cProfile.Profile()
            # profile.enable()

            print(f"================================= generation_index ========= {generation_index}")

            parasites = self.challengers.get_parasites()
            sorting_networks = self.sorting_networks.get_sorting_networks(generation_index)
            print(f"the size of the test is {len(sorting_networks)} sorting networks and {len(parasites)} parasites")
            calc = len(sorting_networks) * len(parasites)
            print(f"which is {calc:,} calcules for run_tests function")
            
            sorting_network_tests_results, parasites_tests_results = TestsHub.run_tests(sorting_networks, parasites)
            
            self.sorting_networks.tests_results = sorting_network_tests_results
            self.challengers.tests_results = parasites_tests_results

            self.sorting_networks.genetic_algorithm(generation_index)
            self.challengers.genetic_algorithm()

            self.change_elite_percentage(generation_index, 
                                         self.sorting_networks, 
                                         self.challengers)

            gen_time_sec = int(time.time() - gen_time)
            local_gen_time = timedelta(seconds=gen_time_sec)
            print(f"The time for this gen is {local_gen_time}")

            # if self.sorting_networks.best_fitness == 16:
            #     end_count -= 1
            #     if end_count == 0:
            #         break

            # profile.disable()
            # ps = pstats.Stats(profile)
            # ps.sort_stats('cumtime')
            # ps.print_stats(5)

        # ----------- Print Time and Comput Information -----------

        total_time_sec = int(time.time() - sol_time)
        total_time = timedelta(seconds=total_time_sec)
        print(f"The absolute time for this gen is {total_time} sec")
        print(f"The ticks time for this gen is {int(time.perf_counter())}")

        self.sorting_networks.set_best_sorting_networks()
        print("Depth: ", self.sorting_networks.best_individual.score)
        self.sorting_networks.best_individual.console_print_sorting_network()
        self.sorting_networks.best_individual.save_sorting_network_to_file()
        FinalTest.sorting_network_final_test(self.sorting_networks.best_individual, self.challengers)
        return

    def change_elite_percentage(self, generation: int, 
                                pop1: SortingNetworkPopulation, 
                                pop2: UnsolvedSoringPopulation) -> None:
        # const period of generations we switch from exploration to exploitation
        period = 30

        if generation == 0:
            return
        
        # if generation == 299 or generation == 149 or generation == 449 or generation == 29:
        #     pop1.set_elite_percentage(0.2)
        #     pop2.set_elite_percentage(0.4)
        #     return
        
        # if generation/ self.data.max_generations > 0.95:
        #     pop1.set_elite_percentage(0.2)
        #     pop2.set_elite_percentage(0.4)
        #     return
        
        if generation / self.data.max_generations < 0.5:
            pop1.set_mutation_percentage(0.8)
        else:
            pop1.set_mutation_percentage(0.1)


            
        if generation % period == period -1:
            pop1.set_elite_percentage(0.2)
            pop2.set_elite_percentage(0.4)
            return
        
        if generation % period == 0:
            if generation/period % 2:
                exploration_mode = False
            else:
                exploration_mode = True
            
            if exploration_mode:
                pop1.set_elite_percentage(0.08)
                pop2.set_elite_percentage(0.03)
            else:
                pop1.set_elite_percentage(0.03)
                pop2.set_elite_percentage(0.08)

        return
    
    def print_solution_as_network(self) -> None:
        SVG_SortingNetwork.SVG_print_sorting_network(self.sorting_networks.best_individual)
        return
    