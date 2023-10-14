# ----------- Project Files -----------
import SmartInit
# ----------- Consts ----------
inputs_text_sorting_list_size = "enter the size of the problem vector you want to solve: 8 or 16 \n"

user_input = False
                    # size of input (8 or 16) | use smart init (True or False) | size of pop | generation number
setting_vector_8 = [8, False, 2000, 10000]
setting_vector_16 = [16, True, 500, 40000]


class Data:
    sorting_list_size: int
    population_size: int
    max_generations: int
    num_comparators_init_vector: int
    ideal_num_comparators: int
    initial_soring_network_elite_percentage: float
    initial_parasites_elite_percentage: float
    use_smart_init: bool
    setting_vector: list

    def __init__(self):
        if user_input:
            self.init_with_user_input()
        else:
            self.setting_vector = setting_vector_16

        self.init_with_settings()
        self._init_consts()
        self._init_smart_consts()
        return

    def init_with_user_input(self):
        if int(input(inputs_text_sorting_list_size)) == 8:
            self.setting_vector = setting_vector_8
        else:
            self.setting_vector = setting_vector_16
        return

    def init_with_settings(self):
        self.sorting_list_size = self.setting_vector[0]
        self.use_smart_init = self.setting_vector[1]
        self.population_size = self.setting_vector[2]
        self.max_generations = self.setting_vector[3]
        return

    def _init_consts(self):
        if self.sorting_list_size == 16:
            self.initial_unsolved_soring_network_elite_percentage = 0.1
            self.initial_parasites_elite_percentage = 0.1
        elif self.sorting_list_size == 8:
            self.initial_unsolved_soring_network_elite_percentage = 0.01
            self.initial_parasites_elite_percentage = 0.01
        return
    
    # the extra value we get from known articles in the fild
    def _init_smart_consts(self):     
        if self.sorting_list_size == 16:
            self.num_comparators_init_vector = SmartInit.num_comparators_init_vector_16
            self.ideal_num_comparators = SmartInit.ideal_num_comparators_vector_16
        elif self.sorting_list_size == 8:
            self.num_comparators_init_vector = SmartInit.num_comparators_init_vector_8
            self.ideal_num_comparators = SmartInit.ideal_num_comparators_vector_8
        return
