inputs_text_num_genes = "enter the size of the gen:\nFor String enter 13\nFor N-Queens enter 8\nFor BinPacking enter 0\nFor Cartesian enter 2\n"

class Data:

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
        self.num_genes = setting_vector
        return

    def _init_consts(self):
        self.pop_size = 100
        self.max_generations = 100      
        return
