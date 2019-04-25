from abc import ABC, abstractmethod


class AbstractPlayer(ABC):

    @abstractmethod
    def get_move(self):
        pass

    @abstractmethod
    def reset(self):
        pass
