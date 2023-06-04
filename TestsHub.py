# ----------- Project Files -----------
from Comparator import Comparator
from Parasite import Parasite
from SortingNetworkHandler import SortingNetwork
import SortingNetworkHandler
# ----------- Python Package -----------
import numpy as np
# ----------- Consts ----------


def run_tests(sorting_networks: list, parasites: list) -> tuple:

    for i, sorting_network in enumerate(sorting_networks):
        parasites_copy = []
        for j, p_x in enumerate(parasites):
            parasites_copy.append(p_x.copy())
        
        sorting_network.score_test = 0
        for k, p_y in enumerate(parasites_copy):
            test_sol_with_list(sorting_network, p_y)
                
    return sorting_networks, parasites


def test_sol_with_list(sorting_network: SortingNetwork, parasite: Parasite) -> None:
    unsorted_list = parasite.unsorted_list
    unsorted_list_copy = unsorted_list.copy()
    unsorted_list_copy.sort()

    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, unsorted_list)

    success_rate = sum([unsorted_list_copy[i] == unsorted_list[i] for i in range(len(unsorted_list))])
    sorting_network.score_test += success_rate/len(unsorted_list)
    # parasite.score_test += 1 - (success_rate/len(unsorted_list))
    return


def comper_n_swap(comperator: Comparator, lst: list) -> None:
    x = comperator.value[0]
    y = comperator.value[1]

    if lst[x] <= lst[y]:
        comperator.score += 0
        return
    
    if lst[x] > lst[y]:
        temp = lst[x]
        lst[x] = lst[y]
        lst[y] = temp
        comperator.score += 1
        return
