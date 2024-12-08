import random

"""
Defines players for Connect 4, against which MCTS can be tested
"""
class RandomPlayer:
    def randomMove(self, game):
        """
        Choose a random move to make.
        """
        return random.choice(game.getLegalMoves())

class HumanPlayer:
    def move(self, game):
        """
        Allow person to select a legal move.
        """
        legalMoves = game.getLegalMoves()
        print(f"Legal moves: {legalMoves}")  # Display the legal moves

        while True:
            try:
                move = int(input(f"Enter a column number to drop your piece: "))
                if move in legalMoves:
                    return move
                else:
                    print(f"Failed: column {move} is an invalid column. Try again.")
            except ValueError:
                print(f"Failed: input is not an integer. Try again.")
                