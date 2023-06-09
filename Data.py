# ----------- Project Files -----------
import SmartInit


inputs_text_sorting_list_size = "enter the size of the vectors: \n"


class Data:
    sorting_list_size: int
    population_size: int
    max_generations: int
    smart_init_vector: list
    num_comparators_init_vector: int
    initial_soring_network_elite_percentage: float
    initial_parasites_elite_percentage: float

    def __init__(self, setting_vector=None):
        if setting_vector:
            self.init_with_settings(setting_vector)
        else:
            self.init_with_user_input()

        self._init_consts()
        return

    def init_with_user_input(self):
        self.sorting_list_size = int(input(inputs_text_sorting_list_size))
        self.init_smart_vector()
        return

    def init_with_settings(self, setting_vector):
        self.sorting_list_size = setting_vector[0]
        self.init_smart_vector()
        return

    def _init_consts(self):
        self.population_size = 4000
        self.max_generations = 600
        self.initial_unsolved_soring_network_elite_percentage = 0.01
        self.initial_parasites_elite_percentage = 0.01
        return

    def init_smart_vector(self):
        if self.sorting_list_size == 16:
            self.num_comparators_init_vector = SmartInit.num_comparators_init_vector_16
        elif self.sorting_list_size == 8:
            self.num_comparators_init_vector = SmartInit.num_comparators_init_vector_8

        return
