from Comparator import Comparator
from Parasite import Parasite
from SortingNetworkHandler import SortingNetwork
from UnsolvedSoringPopulation import UnsolvedSoringPopulation
# ----------- Python Package -----------

master_test = []


def sorting_network_final_test(sorting_network: SortingNetwork, size_of_problem: int) -> bool:
    global master_test

    accuracy = 0
    success_tests = 0
    set_master_test(size_of_problem)

    print(f"---------- start tests ----------")
    
    for test in master_test:
        success_tests += test_network_with_list(sorting_network, test)

    print("Tests sorted correctly: ", success_tests)
    print("Tests WAS NOT sorted correctly: ", len(master_test) - success_tests)
    print(f"finish with tests !")
    print(f"====================")
    accuracy = (success_tests / (len(master_test))) * 100
    print(f"Tests sorted correctly with accuracy: {round(accuracy, 3)}%")

    if accuracy == 100:
        return True
    return False


def set_master_test(num: int) -> None:
    global master_test
    master_test = []
    create_master_test(num)
    # print(f"master_test len -> {len(master_test)}")
    # print(f"master_test -> {master_test}")
    return


def test_network_with_list(sorting_network: SortingNetwork, unsolved_list: list) -> int:
    for k, comperator in enumerate(sorting_network.gen):
        comper_n_swap(comperator, unsolved_list)

    if check_solved_bits_list(unsolved_list):
        return 1

    # print("the following test wasn't sorted correctly !")
    # print(f"the test => {origin_test}")
    # print(f"the result => {unsolved_list} ------ unsolved !")
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


def check_solved_bits_list(bits_list: list) -> bool:
    n = len(bits_list)
    for i in range(1, n):
        if bits_list[i] < bits_list[i - 1]:
            return False
    return True


def create_master_test(num: int) -> None:
    number_of_tests = 2 ** num
    print(f"number_of_tests -> {number_of_tests}")
    for test in range(number_of_tests):
        master_test.append(int_to_bits(test, num))
    return


def int_to_bits(num, length):
    binary_string = bin(num)[2:]
    binary_string = binary_string.zfill(length)
    bits_list = [int(bit) for bit in binary_string]
    return bits_list