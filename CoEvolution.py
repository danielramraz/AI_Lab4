# ----------- Project Files -----------
from Data import Data
import SortingNetworkPopulation
import TestHub
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
import SortingNetwork
# ----------- Python Package -----------
import time
import threading
# ----------- Consts ----------
setting_vector = [6]


class CoEvolution:
    data: Data
    sorting_networks: SortingNetworkPopulation
    challengers: UnsolvedSoringPopulation
    # testing: TestHub
    solution: SortingNetwork

    def __init__(self) -> None:
        self.data = Data(setting_vector)
        self.challengers = UnsolvedSoringPopulation(self.data)
        # self.testing = TestHub()
        return

    def solve_sorting_network_problem(self) -> None:
        for generation in range(self.data.max_generations):
            parasites = self.challengers.get_parasites()
            sorting_networks = self.sorting_networks.get_sorting_networks()
            
            sorting_network_tests_results, parasites_tests_results = self.run_tests(parasites, sorting_networks)
            
            self.sorting_networks.tests_results = sorting_network_tests_results
            self.challengers.tests_results = parasites_tests_results
        return
    
    def print_solution_as_network(self) -> None:
        
        return

    def run_tests(self, parasites, sorting_networks) -> None:
    
        return
