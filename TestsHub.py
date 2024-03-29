# ----------- Project Files -----------
from Comparator import Comparator
from Parasite import Parasite
from SortingNetworkHandler import SortingNetwork


def run_tests(sorting_networks: list, parasites: list) -> tuple:

    for i, sorting_network in enumerate(sorting_networks):
        parasites_copy = []
        sorting_network.score_test = 0

        for c, comperator in enumerate(sorting_network.gen):
            comperator.score = 0

        for j, p_x in enumerate(parasites):
            parasites_copy.append(p_x.copy())

        for k, p_y in enumerate(parasites_copy):
            test_sol_with_list(sorting_network, p_y)

        sorting_network.score_test = sorting_network.score_test / len(parasites)

    for j, parasite in enumerate(parasites):
        parasite.score_test = parasite.score_test / len(sorting_networks)
                
    return sorting_networks, parasites


def test_sol_with_list(sorting_network: SortingNetwork, parasite: Parasite) -> None:

    local_unsorted_list = parasite.unsorted_list
    list_len = len(local_unsorted_list)
    sorted_list = list(range(list_len))

    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, local_unsorted_list)

    after_sort_score = sum([1 for i in range(list_len) if local_unsorted_list[i] == sorted_list[i]])
    sorting_network.score_test += after_sort_score
    parasite.score_test += (list_len - after_sort_score)
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


