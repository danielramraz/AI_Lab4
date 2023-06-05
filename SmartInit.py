from Comparator import Comparator

init_vector_16 = [
    [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15]],
    [[0, 2], [1, 3], [4, 6], [5, 7], [8, 10], [9, 11], [12, 14], [13, 15]],
    [[0, 4], [1, 5], [2, 6], [3, 7], [8, 12], [9, 13], [10, 14], [11, 15]],
    [[0, 8], [1, 9], [2, 10], [3, 11], [4, 12], [5, 13], [6, 14], [7, 15]]
]
num_comparators_init_vector_16 = 32
ideal_num_comparators_vector_16 = 60


def smart_vector_16():
    smart_init_vector_16 = []
    for phase in init_vector_16:
        for item in phase:
            comparator = Comparator(item)
            smart_init_vector_16.append(comparator)

    return smart_init_vector_16


init_vector_8 = [
    [[0, 1], [2, 3], [4, 5], [6, 7]],
    [[0, 2], [1, 3], [4, 6], [5, 7]],
    [[0, 4], [1, 5], [2, 6], [3, 7]]
]
num_comparators_init_vector_8 = 12
ideal_num_comparators_vector_8 = 19


def smart_vector_8():
    smart_init_vector_8 = []
    for phase in init_vector_16:
        for item in phase:
            comparator = Comparator(item)
            smart_init_vector_8.append(comparator)

    return smart_init_vector_8
