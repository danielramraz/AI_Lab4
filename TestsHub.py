# ----------- Project Files -----------
# ----------- Python Package -----------
import numpy as np
# ----------- Consts ----------



def run_tests(self, parasites, sorting_networks) -> tuple:
    test_score: np.array
    for i, sorting_network in enumerate(sorting_networks):
        for k, parasite in enumerate(parasites):
            test_score += self.test_sol_with_list(sorting_network, parasite)
        print(f"the total score for this sorting network is {test_score}")
    
    return

def test_sol_with_list(sorting_network, parasite) -> np.array:
    score = []
    unsorted_array = parasite

    for i, phase in enumerate(sorting_network):
        for k, swap_cmd in enumerate(phase):
            unsorted_array, sub_Score = swap(swap_cmd[0], swap_cmd[1], unsorted_array)
            score.append(sub_Score)
    
    score = np.array(score)
    print(f"the score is {score}")
    return score
    
def swap(x, y, array) -> tuple:
    if array[x] >= array[y]:
        return array , 0
    if array[x] < array[y]:
        temp = array[x]
        array[x] = array[y]
        array[y] = temp
        return array , 1




