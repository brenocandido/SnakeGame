
class Score:

    def __init__(self, food_value = 20, moves_to_decrement = 20, score_decrement = 1):
        self.score = 0
        self.food_value = food_value
        self.moves_to_decrement = moves_to_decrement
        self.score_decrement = score_decrement
        self.move_count = 0
        self.eat_flag = False

    def reset(self):
        self.score = 0
        self.move_count = 0
        self.eat_flag = False

    def move_increment(self):
        self.move_count += 1

    def check_decrement(self):
        if self.move_count != 0 and self.move_count % self.moves_to_decrement == 0:
            new_score = self.score - self.score_decrement
            self.score = new_score if new_score >= 0 else 0

    def eat(self):
        self.eat_flag = True

    def food_increment(self):
        if self.eat_flag:
            self.score = self.score + self.food_value

        self.eat_flag = False

    def refresh(self):
        self.move_increment()
        self.check_decrement()
        self.food_increment()
