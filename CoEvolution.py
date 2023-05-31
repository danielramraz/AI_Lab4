# ----------- Project Files -----------
import numpy as np
from Data import Data
from SortingNetworkPopulation import SortingNetworkPopulation
import TestHub
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
import SortingNetwork
import TestsHub
# ----------- Python Package -----------
import time
import threading
# ----------- Consts ----------
setting_vector = [16]


class CoEvolution:
    data: Data
    sorting_networks: SortingNetworkPopulation
    challengers: UnsolvedSoringPopulation
    solution: SortingNetwork

    def __init__(self) -> None:
        self.data = Data(setting_vector)
        self.challengers = UnsolvedSoringPopulation(self.data)
        self.sorting_networks = SortingNetworkPopulation(self.data)
        
        return

    def solve_sorting_network_problem(self) -> None:
        for generation in range(self.data.max_generations):
            self.sorting_networks.genetic_algorithm()
            parasites = self.challengers.get_parasites()
            sorting_networks = self.sorting_networks.get_sorting_networks()
            
            sorting_network_tests_results, parasites_tests_results = TestsHub.run_tests(sorting_networks, parasites)
            
            self.sorting_networks.tests_results = sorting_network_tests_results
            self.challengers.tests_results = parasites_tests_results

            self.sorting_networks.genetic_algorithm()
            self.challengers.genetic_algorithm()
        return
    
    def print_solution_as_network(self) -> None:
        
        return
