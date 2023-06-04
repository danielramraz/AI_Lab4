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
    local_unsorted_list = parasite.unsorted_list
    # unsorted_list_copy = local_unsorted_list.copy()
    # unsorted_list_copy.sort()
    soved_list = range(len(local_unsorted_list))

    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, local_unsorted_list)

    # success_rate = sum([soved_list[i] == local_unsorted_list[i] for i in range(len(local_unsorted_list))])
    # sorting_network.score_test += success_rate/len(local_unsorted_list)
    
    # parasite.score_test += 1 - (success_rate/len(unsorted_list))

    # the new score for the network is the dif in the inputs befor and after the attempt of sorting
    after_sort_score = fitness(local_unsorted_list)
    sorting_network.score_test += (parasite.score - after_sort_score)
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


def fitness(gen: list) -> float:
    score = 0
    for i in range(len(gen)):
        for j in range(i + 1, len(gen)):
            if gen[i] > gen[j]:
                score += 1
    return score
