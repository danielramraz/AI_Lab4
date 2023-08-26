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
from datetime import timedelta


class CoEvolution:
    data: Data
    sorting_networks: SortingNetworkPopulation
    challengers: UnsolvedSoringPopulation
    solution: SortingNetworkHandler

    def __init__(self) -> None:
        self.data = Data()
        self.challengers = UnsolvedSoringPopulation(self.data)
        self.sorting_networks = SortingNetworkPopulation(self.data)

        return

    def solve_sorting_network_problem(self) -> None:
        sol_time = time.time()

        for generation_index in range(self.data.max_generations):
            gen_time = time.time()

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


            self.change_elite_and_mutation_percentage(generation_index,
                                                      self.sorting_networks,
                                                      self.challengers)

            gen_time_sec = int(time.time() - gen_time)
            local_gen_time = timedelta(seconds=gen_time_sec)
            print(f"The time for this gen is {local_gen_time}")

            if self.sorting_networks.best_individual.score_test == self.data.sorting_list_size:
                if FinalTest.sorting_network_final_test(self.sorting_networks.best_individual, 
                                                        self.data.sorting_list_size):
                    break

        # ----------- Print Graphs , Time and Comput Information -----------

        total_time_sec = int(time.time() - sol_time)
        total_time = timedelta(seconds = total_time_sec)

        self.sorting_networks.best_individual.console_print_sorting_network()

        self.sorting_networks.plot_score_graph()
        print(f"The absolute time for this algorithem is {total_time} ")
        # print(f"The ticks time for this algorithem is {int(time.perf_counter())}")

        self.sorting_networks.set_best_sorting_network()
        self.sorting_networks.best_individual.save_sorting_network_to_file(self.data.sorting_list_size)
        
        finished = FinalTest.sorting_network_final_test(self.sorting_networks.best_individual, self.data.sorting_list_size)
        return

    def change_elite_and_mutation_percentage(self, generation: int,pop1: SortingNetworkPopulation,pop2: UnsolvedSoringPopulation) -> None:
        # const period of generations we switch from exploration to exploitation
        period = 30
        progress: float = generation / self.data.max_generations

        if generation == 0:
            return

        if generation % period == period - 1:
            pop1.set_elite_percentage(0.4)
            pop2.set_elite_percentage(0.4)
            return

        if generation % period == 0:
            if generation / period % 2:
                exploration_mode = False
            else:
                exploration_mode = True

            if exploration_mode:
                pop1.set_elite_percentage(0.2)
                pop2.set_elite_percentage(0.1)
            else:
                pop1.set_elite_percentage(0.1)
                pop2.set_elite_percentage(0.2)

        return

    def print_solution_as_network(self) -> None:
        SVG_SortingNetwork.SVG_print_sorting_network(self.sorting_networks.best_individual)
        return
    