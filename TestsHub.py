# ----------- Project Files -----------
from Comparator import Comparator
from Parasite import Parasite
from SortingNetworkHandler import SortingNetwork
import SortingNetworkHandler
# ----------- Python Package -----------
import numpy as np
# ----------- Consts ----------


def run_tests(sorting_networks: list, parasites: list) -> tuple:
    # parasites_copy = []
    # for h in range(len(sorting_networks)):
    #     parasites_copy.append(parasites.copy())
    
    # for h in range(len(sorting_networks)):
    #     for r in range(len(parasites_copy[h])):
    #         print(f"the parasites copy: {parasites_copy[h][r].unsorted_list}")

    for i, sorting_network in enumerate(sorting_networks):
        # print(f"====================== sorting_network index = {i}")
        parasites_copy = []
        for j, p_x in enumerate(parasites):
            parasites_copy.append(p_x.copy())
        
        # for r, p_x in enumerate(parasites_copy):
        #     print(f"the parasites copy: {p_x.unsorted_list}")
        sorting_network.score_test = 0
        for k, p_y in enumerate(parasites_copy):
            test_sol_with_list(sorting_network, p_y)
        
        # test_score = []
        # for j, phase in enumerate(sorting_network.gen):
        #     for k, comperator in enumerate(phase):
        #         test_score.append(comperator.score)
        
        # print(f"{i} the sorting network is ")
        # sorting_network.print_sorting_network()
        # print(f"{i} the total score for this sorting network is {test_score}")
        
    return sorting_networks, parasites


def test_sol_with_list(sorting_network: SortingNetwork, parasite: Parasite) -> None:
    # print(f"the un-solved parasite is {parasite.unsorted_list}")
    # print(f"the sorting network is ")
    # sorting_network.print_sorting_network()

    unsorted_list = parasite.unsorted_list
    unsorted_list_copy = unsorted_list.copy()
    unsorted_list_copy.sort()
    # ------ בניית גן לפי bins -------
    # for i, phase in enumerate(sorting_network.gen):
    #     for k, comperator in enumerate(phase):
    #         comper_n_swap(comperator, unsorted_list)

    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, unsorted_list)

    # print("the solved parasite is: ", unsorted_list)
    success_rate = sum([unsorted_list_copy[i] == unsorted_list[i] for i in range(len(unsorted_list))])
    sorting_network.score_test += success_rate/len(unsorted_list)
    # parasite.score_test += 1 - (success_rate/len(unsorted_list))

    # print(f"the sorting network after is ")
    # sorting_network.print_sorting_network()

    return


def comper_n_swap(comperator: Comparator, lst: list) -> None:
    # print(f"the comperator is {comperator.value}")
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
