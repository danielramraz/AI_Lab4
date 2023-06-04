# ----------- Python Package -----------
import numpy as np
# ----------- Consts Name  -----------
SIGMA_SHARE = 13


def shared_fitness_cluster(population: list):
    similarity_matrix = similarity_matrix_init(population)
    niches = []
    for i, ind in enumerate(population):
        found_niche = False
        for niche in niches:
            for j, niche_ind in enumerate(niche):
                dist = similarity_matrix[i][j]
                if dist < SIGMA_SHARE:
                    niche.append(ind)
                    found_niche = True
                    break
            if found_niche:
                break
        if not found_niche:
            # If no niche found, create a new niche with the current individual
            niches.append([ind])

    return niches


def similarity_matrix_init(population: list):
    matrix = np.zeros((len(population), len(population)))
    for i in range(len(population)):
        for j in range(len(population)):
            matrix[i][j] = population[i].distance_func(population[j])

    return matrix
