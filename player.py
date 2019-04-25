from abstract_player import AbstractPlayer
import pygame
from snake import Direction


class Player(AbstractPlayer):

    def __init__(self):
        self.event_buffer = []*2
        self.__set_event__()

    def get_move(self):
        return self.__get_direction__()

    def __get_direction__(self):
        event = self.__get_event__()
        new_direction = Direction.none

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_direction = Direction.up
            elif event.key == pygame.K_RIGHT:
                new_direction = Direction.right
            elif event.key == pygame.K_DOWN:
                new_direction = Direction.down
            elif event.key == pygame.K_LEFT:
                new_direction = Direction.left

        return new_direction

            # if not self.is_backwards_move(self.snake.direction, new_direction):
            #     self.snake.turn(new_direction)

    def __get_event__(self):
        for event in self.event_buffer:
            if event == pygame.NOEVENT:
                del self.event_buffer[0]

        if len(self.event_buffer) == 0:
            self.event_buffer = pygame.event.get()[0:1]
        else:
            pygame.event.clear()

        event = self.event_buffer.pop(0) if len(self.event_buffer) != 0 else pygame.event.Event(pygame.NOEVENT)
        return event

    def __set_event__(self):
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.QUIT)

    def reset(self):
        pygame.event.clear()
