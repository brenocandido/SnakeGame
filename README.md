# SnakeGame

SnageGame using python's PyGame.
The objective is to create an AI to play snake. Two were developed:
- A-star (A*)
- Neural Network with Genetic Algorithm

The code got a little crowded as it evolved, so don't mind it.

To play normally, run snakegame.py. It's parameters are at the end of the file. Increase the delay if it's too fast.
To use A*, set the human_player flag in snakegame.py to false. It's slow when the game board is too big.
The A* algorithm is almost generic, as it's still required to know the SnakeGame board.

For the Neural Network, run genetic_snakegame.py. The parameters are at the end of the file.
Fitness is calculated in score.py, in the get_final_score method. Be aware that the score isn't necessarily the final fitness, and it can also be decremented and incremented based on snake movement. That was a choice to make learning faster.
The neural network and genetic algorithm itself were implemented in its own files. They are generic. The neural network recieves the number of hidden layers in a list, as 2 hidden layers with 4 and 3 nodes, respectively, would mean [4, 3].
You can increase or decrease the delay during training using up and down arrows, or use set speeds using numbers 1 to 4.

The training itself isn't perfect, as sometimes it takes a while to learn, or doesn't learn at all. Even though some snakes could get quite big.
As it is, the network has 11 inputs (7 sensors, and 4 for food position). The sensors will get any obstacle distance, that can be the snake body or a wall. The food position is left, right, front, or back; all based on current snake direction. The inputs are positive and normalized between 1 and 0, the distance being divided by the board size.
The weights in the Neural Network class are in a list, as each element of the list is a layer. In order to train, they are set to an array form to make things easier.
The snake with the highest fitness has it's weights saved to a file, and if there is a file already created, it'll be overwritten, so be careful with that. Also, if the fitness is exponential, a random snake can have a high fitness based on luck, and might not be the best snake yet.
