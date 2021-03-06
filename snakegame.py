import pygame
import snake
from food import Food
import game_box
import score
from snake import Direction
from player import Player
from player_ai_astar import PlayerAIAStar
from game_box import Item


class Game:
    def __init__(self, screen_size=20, delay=200, box_width=20, human_player=True,
                 food_value=200, moves_to_decrement=1, score_decrement=2, score_decrement_move=2,
                 score_increment=2, initial_score=100, score_tracking=False, turn_decrement_factor=1):
        self.is_running = False

        self.__screen_size__ = screen_size
        self.__box_width__ = box_width
        self.__hit__ = False

        screen_width = screen_size * box_width
        pygame.init()
        self.clock = pygame.time.Clock()

        self.score_tracking = score_tracking
        self.score = score.Score(food_value=food_value, moves_to_decrement=moves_to_decrement,
                                 score_decrement=score_decrement, initial_score=initial_score,
                                 score_increment=score_increment, score_decrement_move=score_decrement_move,
                                 turn_decrement_factor=turn_decrement_factor)

        self.game_box = game_box.GameBox(screen_size)
        self.screen = pygame.display.set_mode([screen_width, screen_width])
        self.walls_list = []
        self.spawn_walls()

        self.snake = None
        self.food = None
        self.player = None
        self.human_player = human_player
        self.setup_game()

        self.__delay__ = delay
        self.is_running = True

        self.__snake_color__ = [0, 0, 0]
        self.__screen_color__ = [255, 255, 255]
        self.__food_color__ = [255, 0, 0]
        self.__wall_color__ = [50, 50, 50]

        # Size tracking
        self.total_size = 0
        self.largest_snake = 0
        self.average_size = 0

        # Check if snake turned
        self.turned = False

    def setup_game(self):
        self.snake = self.spawn_snake((self.__screen_size__//2, self.__screen_size__//2), self.game_box)
        self.food = self.spawn_food()
        self.player = Player() if self.human_player else PlayerAIAStar(self.snake, self.food,
                                                                       self.game_box, self.walls_list)

    @staticmethod
    def spawn_snake(position, game_box):
        _snake = snake.Snake(position, game_box)
        return _snake

    def run(self):
        self.draw()
        while self.is_running:
            pygame.time.wait(self.__delay__)
            self.play()

        pygame.quit()

    def play(self):
        self.snake.start()
        if not self.snake.is_dead():
            self.play_turn()
            self.check_food()

        else:
            pygame.time.wait(1000)
            self.reset()

        self.draw()

    def check_food(self):
        if self.is_on_food():
            self.eat_food()

    def play_turn(self):
        if not self.check_player_quit():
            self.get_player_move()
            self.move()
            self.score.refresh()

    def check_player_quit(self):
        if pygame.event.peek(pygame.QUIT):
            self.is_running = False

            return True

        if not self.human_player:
            pygame.event.clear()
        return False

    def get_player_move(self):
        move = self.player.get_move()
        if not self.is_backwards_move(self.snake.direction, move) and self.snake.is_moving():
            self.check_turned(move)
            self.snake.turn(move)

        return move

    def check_turned(self, move):
        if move != self.snake.direction:
            self.turned = True
        else:
            self.turned = False

    def move(self):
        if self.snake.is_moving():
            new_position = self.new_position(self.snake.direction)

            if not self.check_hit(new_position):
                self.snake.move_head(new_position)

            if not self.__hit__:

                if not self.snake.size_up and self.snake.is_moving():
                    self.snake.decrease_size()
                else:
                    self.snake.size_up = False

            else:
                self.snake_death()

    def new_position(self, move):
        if move == Direction.up or move == Direction.down:  # Vertical move
            k = -1 if move == Direction.up else 1  # Inverted because of screen starting point
            new_position = (self.snake.head().position[0], self.snake.head().position[1] + k)

        else:  # Horizontal move
            k = 1 if move == Direction.right else -1
            new_position = (self.snake.head().position[0] + k, self.snake.head().position[1])

        return new_position

    def snake_death(self):
        self.snake.kill()
        if self.score_tracking:
            self.score_track()

    def eat_food(self):
        self.snake_ate()
        self.score.eat()

    def snake_ate(self):
        self.snake.eat()
        self.food = self.spawn_food()

    def spawn_food(self):
        food = Food(self.game_box.get_unoccupied_list())
        self.game_box.set_item(food.position, Food)
        if self.is_running and not self.human_player:
            self.player.update_food(food)
        return food

    def spawn_walls(self):
        self.walls_list.clear()
        side = self.__screen_size__
        for i in range(side):
            self.__insert_wall__((0, i))
            self.__insert_wall__((side - 1, i))
            self.__insert_wall__((i, 0))
            self.__insert_wall__((i, side - 1))

    def __insert_wall__(self, position):
        if position not in self.walls_list:
            self.walls_list.append(position)
            self.game_box.set_item(position, Item.wall)

    def is_on_food(self):
        return self.food.position == self.snake.head().position

    def check_wall_hit(self, position):
        if position in self.walls_list:
            return True

        return False

    def check_collision(self, position):
        for part in self.snake.body:
            if part != self.snake.head():
                if part.position == position:
                    return True

        return False

    def check_hit(self, position):
        if self.check_collision(self.snake.head().position) or self.check_wall_hit(position):
            self.__hit__ = True
            return True

        return False

    @staticmethod
    def is_backwards_move(current_direction, new_direction):
        if current_direction.value + new_direction.value == 0:
            return True

        return False

    def draw(self):
        self.screen.fill(self.__screen_color__)
        self.draw_food()
        self.draw_walls()
        self.draw_snake()
        self.display_score()
        pygame.display.update()

    def display_score(self):
        self.set_display_caption(str(int(self.score.score)))

    @staticmethod
    def set_display_caption(caption):
        pygame.display.set_caption(caption)

    def draw_snake(self):
        for part in self.snake.body:
            x1 = part.position[0]*self.__box_width__
            x2 = self.__box_width__
            y1 = part.position[1] * self.__box_width__
            y2 = self.__box_width__
            pygame.draw.rect(self.screen, self.__snake_color__, [x1, y1, x2, y2])

    def draw_walls(self):
        for wall in self.walls_list:
            x1 = wall[0]*self.__box_width__
            x2 = self.__box_width__
            y1 = wall[1] * self.__box_width__
            y2 = self.__box_width__
            pygame.draw.rect(self.screen, self.__wall_color__, [x1, y1, x2, y2])

    def draw_food(self):
        x1 = self.food.position[0]*self.__box_width__
        x2 = self.__box_width__
        y1 = self.food.position[1]*self.__box_width__
        y2 = self.__box_width__
        pygame.draw.rect(self.screen, self.__food_color__, [x1, y1, x2, y2])

    def score_track(self):
        self.score.score_track()
        self.get_largest_snake()
        self.get_average_size()

        print("\n----------------------------------",
              "\nGame:", self.score.total_games,
              "\nScore:", self.score.score,
              "\nHigh score:", self.score.high_score,
              "\nAverage score:", self.score.average_score,
              "\nSnake size:", self.snake.size(),
              "\nLargest snake:", self.largest_snake,
              "\nAverage size:", self.average_size,
              "\n----------------------------------\n")

    def get_largest_snake(self):
        if self.snake.size() > self.largest_snake:
            self.largest_snake = self.snake.size()

    def get_average_size(self):
        self.total_size += self.snake.size()
        self.average_size = self.total_size//self.score.total_games

    def reset(self):
        self.game_box.reset()
        # self.spawn_walls()
        self.snake.reset()
        self.__hit__ = False
        self.food = self.spawn_food()
        self.score.reset()
        self.player.reset()
        self.turned = False


if __name__ == "__main__":
    game = Game(screen_size=20, box_width=20, delay=0, human_player=False, score_tracking=True)
    game.run()
