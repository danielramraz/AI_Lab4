# ----------- Project Files -----------
import numpy as np
from Comparator import Comparator
from Parasite import Parasite
from SortingNetworkHandler import SortingNetwork
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
# ----------- Python Package -----------
import random


parasites_tests = []        # get best parasites
random_tests = []           # 10 random tests
engineered_tests = []       # some spacial cases
sorted_list = []            

def set_local_testing(challengers: UnsolvedSoringPopulation) -> None:

    global sorted_list
    global parasites_tests
    global random_tests
    global engineered_tests
    global sorted_list

    sorted_list = list(range(16))
    parasites_tests = challengers.get_parasites_as_lists()
    for i in range(10):
        unsorted_random_list = list(range(16))
        random.shuffle(unsorted_random_list)
        random_tests.append(unsorted_random_list)

    engineered_examples = [[0,2,4,6,8,10,12,14,15,13,11,9,7,5,3,1],
                            [0,3,6,9,12,15,14,13,11,10,8,7,5,4,2,1],
                            [0,5,10,15,14,13,12,11,9,8,7,6,4,3,2,1],
                            [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
                            [0,15,1,14,2,13,3,12,4,11,5,10,6,9,7,8]]
    
    for index, test in enumerate(engineered_examples):
        engineered_tests.append(test)
        engineered_tests.append(test.copy())
        engineered_tests[index*2].reverse()
   
    return

def sorting_network_final_test(sorting_network: SortingNetwork, challengers: UnsolvedSoringPopulation) -> None:
    global sorted_list
    global parasites_tests
    global random_tests
    global engineered_tests
    global sorted_list

    set_local_testing(challengers)

    print(f"---------- start parasites tests ----------")
    for parasite in parasites_tests:
        test_network_with_list(sorting_network, parasite)
        # print(f"engineered case {parasite}")
    print(f"finish with parasites tests !")

    print(f"---------- start random tests ----------")
    for test in random_tests:
        test_network_with_list(sorting_network, test)
        # print(f"engineered case {test}")
    print(f"finish with random tests !")

    print(f"---------- start engineered tests ----------")
    for case in engineered_tests:
        test_network_with_list(sorting_network, case)
        # print(f"engineered case {case}")
    print(f"finish with engineered tests !")

    print(f"====================\nfinish with all tests !!!!!!!")
    return


def test_network_with_list(sorting_network: SortingNetwork, unsolved_list: list) -> None:
    origin_test = unsolved_list.copy()
    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, unsolved_list)

    if check_solved_list(unsolved_list):
        print("test sorted correctly !")
        return
    
    print("the following test wasn't sorted correctly !")
    print(f"the test => {origin_test}")
    print(f"the result => {unsolved_list} ------ unsolved !")
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

def check_solved_list(lst: list) -> bool:
    if lst == sorted_list:
        return True
    else:
        return False

