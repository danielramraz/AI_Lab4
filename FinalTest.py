# ----------- Project Files -----------
import numpy as np
from Comparator import Comparator
from Parasite import Parasite
from SortingNetworkHandler import SortingNetwork
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
# ----------- Python Package -----------
import random


parasites_tests = []        # get best parasites
random_tests = []           # 100 random tests
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
    accuracy = 0

    print(f"---------- start parasites tests ----------")
    success_tests = 0
    for parasite in parasites_tests:
        success_tests += test_network_with_list(sorting_network, parasite)
        # print(f"engineered case {parasite}")
    print("Tests sorted correctly: ", success_tests)
    print("Tests WAS NOT sorted correctly: ", len(parasites_tests) - success_tests)
    print(f"finish with parasites tests !")
    accuracy += success_tests

    print(f"---------- start random tests ----------")
    success_tests = 0
    for test in random_tests:
        success_tests += test_network_with_list(sorting_network, test)
        # print(f"engineered case {test}")
    print("Tests sorted correctly: ", success_tests)
    print("Tests WAS NOT sorted correctly: ", len(random_tests) - success_tests)
    print(f"finish with random tests !")
    accuracy += success_tests

    print(f"---------- start engineered tests ----------")
    success_tests = 0
    for case in engineered_tests:
        success_tests += test_network_with_list(sorting_network, case)
        # print(f"engineered case {case}")
    print("Tests sorted correctly: ", success_tests)
    print("Tests WAS NOT sorted correctly: ", len(engineered_tests) - success_tests)
    print(f"finish with engineered tests !")
    accuracy += success_tests

    print(f"====================\nfinish with all tests !!!!!!!")
    accuracy = (accuracy / (len(parasites_tests) + len(random_tests) + len(engineered_tests))) * 100
    print(f"Tests sorted correctly with accuracy: {accuracy}%")

    return


def test_network_with_list(sorting_network: SortingNetwork, unsolved_list: list) -> int:
    origin_test = unsolved_list.copy()
    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, unsolved_list)

    if check_solved_list(unsolved_list):
        # print("test sorted correctly !")
        return 1
    
    print("the following test wasn't sorted correctly !")
    print(f"the test => {origin_test}")
    print(f"the result => {unsolved_list} ------ unsolved !")
    return 0


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

