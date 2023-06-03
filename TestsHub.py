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
        for j, phase in enumerate(sorting_network.gen):
            for k, comperator in enumerate(phase):
                test_score.append(comperator.score)
        
        print(f"{i} the sorting network is ")
        sorting_network.print_sorting_network()
        print(f"{i} the total score for this sorting network is {test_score}")
    
    return sorting_networks, parasites

def test_sol_with_list(sorting_network, parasite) -> None:
    # score = []
    unsorted_list = parasite.unsorted_list

    for i, phase in enumerate(sorting_network.gen):
        for k, comperator in enumerate(phase):
            swap(comperator, unsorted_list)
    
    # score = np.array(score)
    # print(f"the score is {score}")
    return
    
def swap(comperator, lst) -> None:
    x = comperator.value[0]
    y = comperator.value[1]

    if lst[x] >= lst[y]:
        comperator.score += 0
        return
    
    if lst[x] < lst[y]:
        temp = lst[x]
        lst[x] = lst[y]
        lst[y] = temp
        comperator.score += 1
        return
