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

def test_sol_with_list(sorting_network, parasite) -> SortingNetwork:
    score = []
    unsorted_array = parasite

    for i, phase in enumerate(sorting_network):
        for k, comperator in enumerate(phase):
            unsorted_array, sub_Score = swap(comperator[0], comperator[1], unsorted_array)
            score.append(sub_Score)
    
    score = np.array(score)
    print(f"the score is {score}")
    return sorting_network
    
def swap(x, y, array) -> tuple:
    if array[x] >= array[y]:
        return array , 0
    if array[x] < array[y]:
        temp = array[x]
        array[x] = array[y]
        array[y] = temp
        return array , 1
