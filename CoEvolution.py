# ----------- Project Files -----------
from Data import Data
from SortingNetworkPopulation import SortingNetworkPopulation
import TestHub
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
from SortingNetworkHandler import SortingNetwork
# ----------- Python Package -----------
import time
import threading
# ----------- Consts ----------
setting_vector = [16]


class CoEvolution:
    data: Data
    sorting_networks: SortingNetworkPopulation
    challengers: UnsolvedSoringPopulation
    testing: TestHub
    solution: SortingNetwork

    def __init__(self) -> None:
        self.data = Data(setting_vector)
        self.challengers = UnsolvedSoringPopulation(self.data)
        self.sorting_networks = SortingNetworkPopulation(self.data)
        
        return

    def solve_sorting_network_problem(self) -> None:
        for generation in range(self.data.max_generations):
            # self.testing.parasites = self.challengers.get_parasites()
            self.sorting_networks.genetic_algorithm()
            # self.testing.sorting_networks = self.sorting_networks.get_sorting_networks()
            # self.testing.run_tests()
            # self.sorting_networks.tests_results = self.testing.get_sorting_network_tests_results()
            # self.challengers.tests_results = self.testing.get_parasites_tests_results()
        return
    
    def print_solution_as_network(self) -> None:
        
        return
