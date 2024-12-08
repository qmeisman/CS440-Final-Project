import random
import math
import time
from connect4 import OUTCOME_ONE, OUTCOME_TWO, OUTCOME_DRAW, PIECE_ONE, PIECE_TWO, PIECE_NONE
from copy import deepcopy

EXPLORATION = math.sqrt(2)
"""
Defines a node in the MCTS, storing state characteristics.
"""
class Node:
    
    def __init__(self, parent, move, gameState):
        self.gameState = gameState # holds the state of the game we are playing (in this case, Connect-4)
        self.N = 0 # total number of simulations 
        self.U = 0 # number of simulations won
        self.UCB1 = float('inf') # UCT value
        self.parent = parent # parent state
        self.children = {} # key: move that led to child state, value: child state
        self.move = move # action that led to this state (choice between columns 0-6)

    def updateUCB1(self, explorationConstant=EXPLORATION):
        """
        Update UCB1 value of node based on U and N.
        """
        if self.N != 0:
            self.UCB1 = self.U / self.N +  explorationConstant * math.sqrt(math.log(self.parent.N) / self.N)

    def addChildren(self, children):
        """
        Assign a list of children to node.
        """
        self.children = children
    
        
"""
Implements the four phases of the Monte Carlo Tree Search. 
"""
class MCTS:
    
    def __init__(self, gameRoot):
        self.root = Node(parent=None, move=None, gameState=deepcopy(gameRoot)) # Initial node state
        
    def select(self):
        """
        Selection phase: Starting at the root of the search tree, a move is chosen
        based on the Upper Confidence Bounds Applied to Trees (UCT) until a leaf node
        is reached.
        """
        currNode = self.root
        
        # If the current node is not a leaf node, keep traversing tree
        while len(currNode.children) != 0:
            children = currNode.children.values()
            maxUCB1 = max(child.UCB1 for child in children)
            # Find children with highest UCB1 value
            maxChildren = [child for child in children if child.UCB1 == maxUCB1]
            # Choose random child from maxChildren to continue the search
            currNode = random.choice(maxChildren)
        return currNode

    def expand(self, leafNode):
        """
        Expansion phase: grow the search tree by generating a new child from the 
        selected node.
        """
        legalMoves = leafNode.gameState.getLegalMoves()

        # Terminal state
        if len(legalMoves) == 0:
            return leafNode

        # Unvisited nodes that are not the node should be simulated
        if leafNode.N == 0 and leafNode is not self.root:
            return leafNode
        # Create children if legal moves exist
        children = {}
        for move in legalMoves:
            parentState = deepcopy(leafNode.gameState)
            if leafNode is not self.root:
                parentState.switchPlayer()
            # Make new child state based on the specific move
            parentState.dropPiece(move) 
            newChild = Node(leafNode, move, parentState)
            children[move] = newChild

        # Expand tree and select a child
        leafNode.addChildren(children)
        selectedChild = list(leafNode.children.values())[0]
        return selectedChild

    def simulate(self, child):
        """
        Simulation/Rollout phase: perform a playout from the newly generated child node,
        resulting in either a win or loss.
        """
        gameCopy = deepcopy(child.gameState)

        # Continue simulation while no player has won and there are still legal moves to be made
        while not gameCopy.isGameOver():
            # Switch the player before the game begans
            gameCopy.switchPlayer()
            # Choose a random action to take
            move = random.choice(gameCopy.getLegalMoves())
            gameCopy.dropPiece(move)
        return gameCopy.getOutcome()
                    
    def backpropagate(self, node, outcome):
        """
        Back-propagation phase: Use the result from the Simulation phase to update the search tree, 
        going all the way up to the root node.
        """
        currNode = node
        # First pass: recalculate N and U
        while currNode is not None:
            # Increment the number of simulations that have taken place through this node
            currNode.N += 1
        
            if outcome == OUTCOME_ONE: 
                if currNode.gameState.player == PIECE_ONE:
                    currNode.U += 1
            elif outcome == OUTCOME_TWO:
                if currNode.gameState.player == PIECE_TWO:
                    currNode.U += 1
            currNode = currNode.parent
            
        # Second pass: Update UCB1 based on new N and U values, skip root
        currNode = node 
        while currNode is not self.root:
            currNode.updateUCB1()
            currNode = currNode.parent
            

    def search(self, timeLimit):
        """
        Perform the MCTS within the specified time.
        """
        startTime = time.process_time()
        numSimulations = 0
        
        while time.process_time() - startTime < timeLimit:
            leafNode = self.select()
            childNode = self.expand(leafNode)
            outcome = self.simulate(childNode)
            self.backpropagate(childNode, outcome)
            numSimulations += 1
        return numSimulations

    def getBestMove(self):
        children = self.root.children.values()
        maxN = max(child.N for child in children)
        maxChildren = [child for child in children if child.N == maxN]
        return random.choice(maxChildren).move
        