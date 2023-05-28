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
    sorting_network: SortingNetworkPopulation
    challengers: UnsolvedSoringPopulation
    testing: TestHub
    solution: SortingNetwork

    def __init__(self) -> None:
        self.data = Data(setting_vector)
        self.challengers = UnsolvedSoringPopulation(self.data)
        
        return

    def solve_sorting_network_problem(self) -> None:

        self.challengers.genetic_algorithem()
        self.challengers.print_population()

        return
    
    def print_solution_as_network(self) -> None:
        
        return
