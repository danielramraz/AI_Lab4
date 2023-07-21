# ----------- Project Files -----------
from Comparator import Comparator
from Parasite import Parasite
from SortingNetworkHandler import SortingNetwork
import SortingNetworkHandler


def run_tests(sorting_networks: list, parasites: list) -> tuple:

    for i, sorting_network in enumerate(sorting_networks):
        parasites_copy = []
        sorting_network.score_test = 0
        # total_score = 0

        for c, comperator in enumerate(sorting_network.gen):
            comperator.score = 0

        for j, p_x in enumerate(parasites):
            parasites_copy.append(p_x.copy())

        for k, p_y in enumerate(parasites_copy):
            test_sol_with_list(sorting_network, p_y)
            # total_score += test_sol_with_list(sorting_network, p_y)

        sorting_network.score_test = sorting_network.score_test / len(parasites)
        # sorting_network.score_test += total_score / len(parasites)
        # sorting_network.tests_counter += 1

    for j, parasite in enumerate(parasites):
        parasite.score_test = parasite.score_test / len(sorting_networks)
                
    return sorting_networks, parasites


def test_sol_with_list(sorting_network: SortingNetwork, parasite: Parasite) -> float:

    local_unsorted_list = parasite.unsorted_list
    sorted_list = list(range(8))

    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, local_unsorted_list)

    # the new score for the network is the dif in the inputs before and after the attempt of sorting
    # after_sort_score = fitness(local_unsorted_list)
    # sorting_network.score_test += (parasite.score - after_sort_score)
    # parasite.score_test -= sorting_network.score_test

    after_sort_score = sum([1 for i in range(len(sorted_list)) if local_unsorted_list[i] == sorted_list[i]])
    sorting_network.score_test += after_sort_score
    parasite.score_test += (8 - after_sort_score)

    # return after_sort_score
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


