
class Score:

    def __init__(self, food_value=200, moves_to_decrement=2, score_decrement=1, score_decrement_move = 1,
                 score_increment=1, initial_score=0, turn_decrement_factor=1):
        self.initial_score = initial_score
        self.score = initial_score
        self.food_value = food_value
        self.moves_to_decrement = moves_to_decrement
        self.score_decrement_step = score_decrement
        self.move_count = 0
        self.eat_flag = False
        self.score_increment_step = score_increment
        self.score_decrement_move = score_decrement_move
        self.turn_decrement_factor = turn_decrement_factor

        self.times_ate_food = 0

        self.total_score = 0
        self.high_score = 0
        self.average_score = 0
        self.total_games = 0

        self.killed_itself = False
        self.killed_itself_penalty = 0.8

        self.times_moved_towards_food = 0
        self.times_moved_away_from_food = 0

        self.spinners = 0

        self.current_high_score = 0

    def reset(self):
        self.score = self.initial_score
        self.move_count = 0
        self.eat_flag = False
        self.current_high_score = 0
        self.times_ate_food = 0
        self.killed_itself = False
        self.times_moved_towards_food = 0
        self.times_moved_away_from_food = 0

    def trackers_reset(self):
        self.spinners = 0

    def move_increment(self):
        self.move_count += 1

    def move_towards_food(self):
        # self.score += self.score_increment_step
        self.times_moved_towards_food += 1

    def move_away_from_food(self):
        # self.score_subtract(self.score_decrement_step)
        self.times_moved_away_from_food += 1

    def check_decrement(self, turned=False):
        if self.move_count != 0 and self.move_count % self.moves_to_decrement == 0:
            if turned:
                k = self.turn_decrement_factor
            else:
                k = 1

            new_score = self.score - self.score_decrement_move * k
            self.score = new_score if new_score >= 0 else 0

    def eat(self):
        self.eat_flag = True
        self.times_ate_food += 1

    def food_increment(self):
        if self.eat_flag:
            self.score = self.score + self.food_value

        self.eat_flag = False

    def score_track(self):
        self.total_games += 1

        self.update_high_score()
        self.calculate_average_score()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def ate_itself(self):
        self.killed_itself = True

    def hit_wall(self):
        self.killed_itself = True

    def score_subtract(self, amount):
        self.score -= amount
        if self.score < 0:
            self.score = 0

    def calculate_average_score(self):
        self.total_score += self.score
        self.average_score = self.total_score//self.total_games

    def get_moves_to_food(self):
        return self.times_moved_towards_food - self.times_moved_away_from_food

    def check_spinner(self):
        if self.score == 0 and self.times_ate_food == 0:
            self.spinners += 1

    def get_final_score(self):

        final_score = 0.5*self.get_moves_to_food()*(self.score*(self.move_count*0.1)*self.times_ate_food)\
                      + (self.times_ate_food**2)*self.food_value

        if final_score < 0:
            final_score = 0

        penalty = self.killed_itself_penalty if self.killed_itself else 1
        return final_score * penalty

    def refresh(self, turned=False):
        self.move_increment()
        self.check_decrement(turned)
        self.food_increment()

        if self.score > self.current_high_score:
            self.current_high_score = self.score
