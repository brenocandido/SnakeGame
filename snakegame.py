import pygame
import snake
from food import Food
import game_box
import score
from snake import Direction
from player import Player
from player_ai import PlayerAI


class Game:
    def __init__(self, screen_size=20, delay=200, box_width=20, human_player=True):
        self.is_running = False
        self.human_player = human_player
        self.__screen_size__ = screen_size
        self.__box_width__ = box_width
        self.__hit__ = False
        self.game_box = game_box.GameBox(screen_size)
        screen_width = screen_size * box_width
        pygame.init()
        self.screen = pygame.display.set_mode([screen_width, screen_width])
        self.snake = self.spawn_snake((screen_size//2, screen_size//2), self.game_box)
        self.food = self.spawn_food()
        self.clock = pygame.time.Clock()
        self.score = score.Score(20, 20, 1)
        self.player = Player() if human_player else PlayerAI(self.snake, self.food, self.score, self.game_box)
        self.__snake_color__ = [0, 0, 0]
        self.__screen_color__ = [255, 255, 255]
        self.__food_color__ = [255, 0, 0]
        self.__delay__ = delay
        self.is_running = True

    def spawn_snake(self, position, game_box):
        _snake = snake.Snake(position, game_box)
        return _snake

    def run(self):
        while self.is_running:
            self.draw()
            pygame.time.wait(self.__delay__)
            self.snake.start()
            if not self.snake.is_dead():
                self.play_turn()
                if self.is_on_food():
                    self.eat_food()
            else:
                pygame.time.wait(1000)
                self.reset()

    def play_turn(self):
        if not self.check_player_quit():
            self.get_player_move()
            self.move()
            self.score.refresh()

    def check_player_quit(self):
        if pygame.event.peek(pygame.QUIT):
            self.is_running = False
            pygame.quit()

            return True

        return False

    def get_player_move(self):
        move = self.player.get_move()
        if not self.is_backwards_move(self.snake.direction, move) and self.snake.is_moving():
            self.snake.turn(move)

    def move(self):
        if self.snake.is_moving():
            if self.snake.direction == Direction.up or self.snake.direction == Direction.down:      # Vertical move
                k = -1 if self.snake.direction == Direction.up else 1           # Inverted because of screen starting point
                new_position = (self.snake.head().position[0], self.snake.head().position[1] + k)
                if not self.check_hit(new_position):
                    self.snake.move_head(new_position)

            else:                                                                        # Horizontal move
                k = 1 if self.snake.direction == Direction.right else -1
                new_position = (self.snake.head().position[0] + k, self.snake.head().position[1])
                if not self.check_hit(new_position):
                    self.snake.move_head(new_position)

            if not self.__hit__:

                if not self.snake.size_up and self.snake.is_moving():
                    self.snake.decrease_size()
                else:
                    self.snake.size_up = False

            else:
                self.snake.kill()

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

    def is_on_food(self):
        return self.food.position == self.snake.head().position

    def check_wall_hit(self, position):
        if 0 <= position[0] < self.__screen_size__ and 0 <= position[1] < self.__screen_size__:
            return False

        return True

    def check_collision(self):
        for part in self.snake.body:
            if part != self.snake.head():
                if part.position == self.snake.head().position:
                    return True

        return False

    def check_hit(self, position):
        if self.check_collision() or self.check_wall_hit(position):
            self.__hit__ = True
            return True

        return False

    def is_backwards_move(self, current_direction, new_direction):
        if current_direction.value + new_direction.value == 0:
            return True

        return False

    def draw(self):
        self.screen.fill(self.__screen_color__)
        self.draw_snake()
        self.draw_food()
        self.set_display_caption(str(self.score.score))
        pygame.display.update()

    def set_display_caption(self, caption):
        pygame.display.set_caption(caption)

    def draw_snake(self):
        for part in self.snake.body:
            x1 = part.position[0]*self.__box_width__
            x2 = self.__box_width__
            y1 = part.position[1] * self.__box_width__
            y2 = self.__box_width__
            pygame.draw.rect(self.screen, self.__snake_color__, [x1, y1, x2, y2])

    def draw_food(self):
        x1 = self.food.position[0]*self.__box_width__
        x2 = self.__box_width__
        y1 = self.food.position[1]*self.__box_width__
        y2 = self.__box_width__
        pygame.draw.rect(self.screen, self.__food_color__, [x1, y1, x2, y2])


    def reset(self):
        self.game_box.reset()
        self.snake.reset()
        self.__hit__ = False
        self.food = self.spawn_food()
        self.score.reset()
        self.player.reset()


game = Game(screen_size=15, delay=15, human_player=False)
game.run()
