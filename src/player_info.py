class PlayerInfo:
    def __init__(self):
        self.reset()

    def reset(self):
        self.name = ""
        self.inning_score = 0
        self.score = 0
        self.service = False

    def increase_inning_score(self):
        self.inning_score = self.inning_score + 1

    def increase_score(self):
        self.score = self.score + 1

    def decrease_score(self):
        if self.score > 0:
            self.score = self.score - 1

    def set_inning_score(self, new_score):
        self.inning_score = self.new_score

    def set_score(self, new_score):
        self.score = self.new_score

    def set_name(self, new_name):
        self.name = new_name

    def set_service(self, my_turn):
        self.service = my_turn

    def copy_from(self, new_info):
        self.name = new_info.name
        self.inning_score = new_info.inning_score
        self.score = new_info.score
        self.service = new_info.service