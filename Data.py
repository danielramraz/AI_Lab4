import itertools

inputs_text_size_vector = "enter the size of the vectors: \n"

class Data:
    all_combinations: list

    def __init__(self, setting_vector = None):
        if setting_vector:
            self.init_with_settings(setting_vector)
        else:
            self.init_with_user_input()

        self._init_consts()
        return

    def init_with_user_input(self):
        self.num_genes = int(input(inputs_text_num_genes))
        return

    def init_with_settings(self, setting_vector):
        # self.num_genes = setting_vector[1]
        self.size_vector = setting_vector
        return

    def _init_consts(self):
        self.pop_size = 100
        self.max_generations = 10
        self.cross_operator = 0

        return
