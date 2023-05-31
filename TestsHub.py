# ----------- Project Files -----------
# ----------- Python Package -----------
import numpy as np

from SortingNetwork import SortingNetwork
# ----------- Consts ----------

def run_tests(sorting_networks, parasites) -> tuple:

    for i, sorting_network in enumerate(sorting_networks):
        parasites_copy = parasites

        for k, parasite in enumerate(parasites_copy):
            test_sol_with_list(sorting_network, parasite)
        
        test_score = []
        test_score = [test_score.append(comp.score) for i, comp in enumerate(sorting_network)]
        print(f"the total score for this sorting network is {test_score}")
    
    return sorting_networks, parasites

def test_sol_with_list(sorting_network, parasite) -> None:
    # score = []
    unsorted_array = parasite

    for i, phase in enumerate(sorting_network):
        for k, comperator in enumerate(phase):
            swap(comperator, unsorted_array)
    
    # score = np.array(score)
    # print(f"the score is {score}")
    return
    
def swap(comperator, array) -> None:
    x = comperator.value[0]
    y = comperator.value[1]

    if array[x] >= array[y]:
        comperator.score += 0
        return
    
    if array[x] < array[y]:
        temp = array[x]
        array[x] = array[y]
        array[y] = temp
        comperator.score += 1
        return
