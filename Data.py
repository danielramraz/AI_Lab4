inputs_text_sorting_list_size = "enter the size of the gen:\nFor String enter 13\nFor N-Queens enter 8\nFor BinPacking enter 0\nFor Cartesian enter 2\n"

class Data:
    sorting_list_size: int
    population_size: int
    max_generations: int

    def __init__(self, setting_vector = None):
        if setting_vector:
            self.init_with_settings(setting_vector)
        else:
            self.init_with_user_input()

        self._init_consts()
        return

    def init_with_user_input(self):
        self.sorting_list_size = int(input(inputs_text_sorting_list_size))
        return

    def init_with_settings(self, setting_vector):
        # self.sorting_list_size = setting_vector[1]
        self.sorting_list_size = setting_vector
        return

    def _init_consts(self):
        self.population_size = 100
        self.max_generations = 10      
        return
