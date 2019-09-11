# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foods = currentGameState.getFood().asList()
        if action == 'Stop':
            return -float("inf")
        for state in newGhostStates:
            if state.getPosition() == newPos:
                if state.scaredTimer == 0:
                    return -float("inf")
        distances = []
        for food in foods:
            dist = manhattanDistance(food, newPos) * -1
            distances.append(dist)
        return max(distances)
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def maximizer_or_minimizer(self, gameState, current_agentIndex, current_depth):
        if not gameState.getLegalActions(current_agentIndex):
            return self.evaluationFunction(gameState)
        if current_agentIndex == 0:
            current_max = ("", -float("inf"))
            for action in gameState.getLegalActions(current_agentIndex):
                if action == "Stop":
                    continue
                minimax = self.minmax(gameState.generateSuccessor(current_agentIndex, action), current_agentIndex+1, current_depth)
                if type(minimax) is tuple:
                    minimax = minimax[1]
                decision = max(minimax, current_max[1])
                if decision == minimax:
                    current_max = (action, decision)
            return current_max
        else:
            current_min = ("", float("inf"))
            for action in gameState.getLegalActions(current_agentIndex):
                if action == "Stop":
                    continue
                minimax = self.minmax(gameState.generateSuccessor(current_agentIndex, action), current_agentIndex+1, current_depth)
                if type(minimax) is tuple:
                    minimax = minimax[1]
                decision = min(minimax, current_min[1])
                if decision == minimax:
                    current_min = (action, decision)
            return current_min

    def minmax(self, gameState, current_agentIndex, current_depth):
        #we cannot have current_agentIndex exceed amount of agents
        if current_agentIndex >= gameState.getNumAgents():
            current_agentIndex = 0
            current_depth += 1
        if current_depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        else:
            return self.maximizer_or_minimizer(gameState, current_agentIndex, current_depth)


    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        current_depth = 0
        current_agentIndex = 0
        final_minmax = self.minmax(gameState, current_agentIndex, current_depth)
        return final_minmax[0]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def maximizer_or_minimizer(self, gameState, current_agentIndex, current_depth, alpha, beta):
        if not gameState.getLegalActions(current_agentIndex):
            return self.evaluationFunction(gameState)
        if current_agentIndex == 0:
            current_max = ("", -float("inf"))
            for action in gameState.getLegalActions(current_agentIndex):
                if action == "Stop":
                    continue
                minimax = self.minmax(gameState.generateSuccessor(current_agentIndex, action), current_agentIndex+1, current_depth, alpha, beta)
                if type(minimax) is tuple:
                    minimax = minimax[1]
                decision = max(minimax, current_max[1])
                if decision == minimax:
                    current_max = (action, decision)
                if current_max[1] > beta:
                    return current_max
                alpha = max(alpha, current_max[1])
            return current_max
        else:
            current_min = ("", float("inf"))
            for action in gameState.getLegalActions(current_agentIndex):
                if action == "Stop":
                    continue
                minimax = self.minmax(gameState.generateSuccessor(current_agentIndex, action), current_agentIndex+1, current_depth, alpha, beta)
                if type(minimax) is tuple:
                    minimax = minimax[1]
                decision = min(minimax, current_min[1])
                if decision == minimax:
                    current_min = (action, decision)
                if current_min[1] < alpha:
                    return current_min
                beta = min(beta, current_min[1])
            return current_min

    def minmax(self, gameState, current_agentIndex, current_depth, alpha, beta):
        #we cannot have current_agentIndex exceed amount of agents
        if current_agentIndex >= gameState.getNumAgents():
            current_agentIndex = 0
            current_depth += 1
        if current_depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        else:
            return self.maximizer_or_minimizer(gameState, current_agentIndex, current_depth, alpha, beta)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float("inf")
        beta = float("inf")
        current_depth = 0
        current_agentIndex = 0
        final_minmax = self.minmax(gameState, current_agentIndex, current_depth, alpha, beta)
        return final_minmax[0]



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def exp_value(self, gameState, current_agentIndex, current_depth):
        current_exp_value = ("", 0)
        if not gameState.getLegalActions(current_agentIndex):
            return self.evaluationFunction(gameState)
        total = len(gameState.getLegalActions(current_agentIndex))
        probability = 1.0 / total
        for action in gameState.getLegalActions(current_agentIndex):
            if action == "Stop":
                continue
            expectimax_value = self.expectimax(gameState.generateSuccessor(current_agentIndex, action), current_agentIndex+1, current_depth)
            if type(expectimax_value) == tuple:
                expectimax_value = expectimax_value[1]
            current_exp_value = (action, current_exp_value[1] + (probability * expectimax_value))
        return tuple(current_exp_value)

    def max_value(self, gameState, current_agentIndex, current_depth):
        current_max = ("", -float("inf"))
        if not gameState.getLegalActions(current_agentIndex):
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(current_agentIndex):
            if action == "Stop":
                continue
            max_value = self.expectimax(gameState.generateSuccessor(current_agentIndex, action), current_agentIndex+1, current_depth)
            if type(max_value) == tuple:
                max_value = max_value[1]
            decision = max(max_value, current_max[1])
            if decision == max_value:
                current_max = (action, decision)
        return current_max


    def expectimax(self, gameState, current_agentIndex, current_depth):
        #we cannot have current_agentIndex exceed amount of agents
        if current_agentIndex >= gameState.getNumAgents():
            current_agentIndex = 0
            current_depth += 1
        if current_depth == self.depth:
            return self.evaluationFunction(gameState)
        if current_agentIndex == 0:
            return self.max_value(gameState, current_agentIndex, current_depth)
        else:
            return self.exp_value(gameState, current_agentIndex, current_depth)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        current_depth = 0
        current_agentIndex = 0
        final_expectimax = self.expectimax(gameState, current_agentIndex, current_depth)
        return final_expectimax[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      My betterEvaluationFunction takes into consideration:
      1) The current score of the gamestate, so the higher the score the better
      2) The closest food to PacMan. The closer the food the better
      3) The closest ghost to PacMan, the closest ghost is the one
         that PacMan must prioritize dodging in order to not lose.
      4) We want to prioritize getting pellets (the larger food that scares ghosts)
         So the sooner PacMan eats the pellets, the less he has to worry about
         dodging ghosts and begins eating (so the evaluation function produces
         better values once pacman begins eating more pellets).

    """
    "*** YOUR CODE HERE ***"
    ghost_distances = []
    ghosts = currentGameState.getGhostStates()
    pellet_distances = []
    pellets = currentGameState.getCapsules()
    food_distances = []
    foods = currentGameState.getFood().asList()
    current_pacman = list(currentGameState.getPacmanPosition())

    for food in foods:
        dist = manhattanDistance(food, current_pacman) * -1
        food_distances.append(dist)
    if len(food_distances) == 0:
        food_distances.append(0)
    best_food_option = max(food_distances)
    optimizable_score = currentGameState.getScore()
    optimize_pellets = len(pellets) * 80

    for ghost in ghosts:
        if ghost.scaredTimer == 0:
            ghost_distances.append(0)
        else:
            dist = manhattanDistance(ghost.getPosition(), current_pacman)
            if dist == 0:
                ghost_distances.append(0)
            else:
                reciprocal = 1.0/(dist)
                ghost_distances.append(-reciprocal)
    best_ghost_option = min(ghost_distances)
    value = optimizable_score + best_food_option + best_ghost_option - optimize_pellets
    return value





# Abbreviation
better = betterEvaluationFunction
