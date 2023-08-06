# ----------- Project Files -----------
import SmartInit
inputs_text_sorting_list_size = "enter the size of the vectors: 8 or 16 \n"
inputs_text_smart_init = "do ypu want to use smart init? 0 = False , 1 = True \n"


class Data:
    sorting_list_size: int
    population_size: int
    max_generations: int
    # smart_init_vector: list
    num_comparators_init_vector: int
    ideal_num_comparators: int
    initial_soring_network_elite_percentage: float
    initial_parasites_elite_percentage: float
    use_smart_init: bool

    def __init__(self, setting_vector = None):
        if setting_vector:
            self.init_with_settings(setting_vector)
        else:
            self.init_with_user_input()

        self._init_consts()
        self._init_smart_consts()
        return

    def init_with_user_input(self):
        self.sorting_list_size = int(input(inputs_text_sorting_list_size))
        self.use_smart_init = bool(input(inputs_text_smart_init))
        
        return

    def init_with_settings(self, setting_vector):
        self.sorting_list_size = setting_vector[0]
        self.use_smart_init = setting_vector[1]
        return

    def _init_consts(self):
        self.population_size = 500
        self.max_generations = 10000
        self.initial_unsolved_soring_network_elite_percentage = 0.1
        self.initial_parasites_elite_percentage = 0.1

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
