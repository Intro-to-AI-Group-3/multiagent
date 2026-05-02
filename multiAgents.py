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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        Starting on 5-1 at 13:31:43

        Question q2
        ===========

        *** PASS: test_cases\q2\0-eval-function-lose-states-1.test
        *** PASS: test_cases\q2\0-eval-function-lose-states-2.test
        *** PASS: test_cases\q2\0-eval-function-win-states-1.test
        *** PASS: test_cases\q2\0-eval-function-win-states-2.test
        *** PASS: test_cases\q2\0-lecture-6-tree.test
        *** PASS: test_cases\q2\0-small-tree.test
        *** PASS: test_cases\q2\1-1-minmax.test
        *** PASS: test_cases\q2\1-2-minmax.test
        *** PASS: test_cases\q2\1-3-minmax.test
        *** PASS: test_cases\q2\1-4-minmax.test
        *** PASS: test_cases\q2\1-5-minmax.test
        *** PASS: test_cases\q2\1-6-minmax.test
        *** PASS: test_cases\q2\1-7-minmax.test
        *** PASS: test_cases\q2\1-8-minmax.test
        *** PASS: test_cases\q2\2-1a-vary-depth.test
        *** PASS: test_cases\q2\2-1b-vary-depth.test
        *** PASS: test_cases\q2\2-2a-vary-depth.test
        *** PASS: test_cases\q2\2-2b-vary-depth.test
        *** PASS: test_cases\q2\2-3a-vary-depth.test
        *** PASS: test_cases\q2\2-3b-vary-depth.test
        *** PASS: test_cases\q2\2-4a-vary-depth.test
        *** PASS: test_cases\q2\2-4b-vary-depth.test
        *** PASS: test_cases\q2\2-one-ghost-3level.test
        *** PASS: test_cases\q2\3-one-ghost-4level.test
        *** PASS: test_cases\q2\4-two-ghosts-3level.test
        *** PASS: test_cases\q2\5-two-ghosts-4level.test
        *** PASS: test_cases\q2\6-tied-root.test
        *** PASS: test_cases\q2\7-1a-check-depth-one-ghost.test
        *** PASS: test_cases\q2\7-1b-check-depth-one-ghost.test
        *** PASS: test_cases\q2\7-1c-check-depth-one-ghost.test
        *** PASS: test_cases\q2\7-2a-check-depth-two-ghosts.test
        *** PASS: test_cases\q2\7-2b-check-depth-two-ghosts.test
        *** PASS: test_cases\q2\7-2c-check-depth-two-ghosts.test
        *** Running MinimaxAgent on smallClassic 1 time(s).
        Pacman died! Score: 84
        Average Score: 84.0
        Scores:        84.0
        Win Rate:      0/1 (0.00)
        Record:        Loss
        *** Finished running MinimaxAgent on smallClassic after 1 seconds.
        *** Won 0 out of 1 games. Average score: 84.000000 ***
        *** PASS: test_cases\q2\8-pacman-game.test

        ### Question q2: 5/5 ###


        Finished at 13:31:45

        Provisional grades
        ==================
        Question q2: 5/5
        ------------------
        Total: 5/5

        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, agentIndex, depth):
            # game is over or depth limti is reached
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            legalActions = gameState.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(gameState)

            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            nextDepth = depth + 1 if nextAgent == 0 else depth

            if agentIndex == 0: # maximizing player 
                return max(minimax(gameState.generateSuccessor(agentIndex, action), nextAgent, nextDepth) for action in legalActions)
            else: # minimizing ghost
                return min(minimax(gameState.generateSuccessor(agentIndex, action), nextAgent, nextDepth) for action in legalActions)

        legalActions = gameState.getLegalActions(0)
        bestAction = None
        maxVal = float('-inf')
        
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = minimax(successor, 1, 0)
            if value > maxVal:
                maxVal = value
                bestAction = action
                
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)

    Starting on 5-1 at 13:32:04

    Question q4
    ===========

    *** PASS: test_cases\q4\0-eval-function-lose-states-1.test
    *** PASS: test_cases\q4\0-eval-function-lose-states-2.test
    *** PASS: test_cases\q4\0-eval-function-win-states-1.test
    *** PASS: test_cases\q4\0-eval-function-win-states-2.test
    *** PASS: test_cases\q4\0-expectimax1.test
    *** PASS: test_cases\q4\1-expectimax2.test
    *** PASS: test_cases\q4\2-one-ghost-3level.test
    *** PASS: test_cases\q4\3-one-ghost-4level.test
    *** PASS: test_cases\q4\4-two-ghosts-3level.test
    *** PASS: test_cases\q4\5-two-ghosts-4level.test
    *** PASS: test_cases\q4\6-1a-check-depth-one-ghost.test
    *** PASS: test_cases\q4\6-1b-check-depth-one-ghost.test
    *** PASS: test_cases\q4\6-1c-check-depth-one-ghost.test
    *** PASS: test_cases\q4\6-2a-check-depth-two-ghosts.test
    *** PASS: test_cases\q4\6-2b-check-depth-two-ghosts.test
    *** PASS: test_cases\q4\6-2c-check-depth-two-ghosts.test
    *** Running ExpectimaxAgent on smallClassic 1 time(s).
    Pacman died! Score: 84
    Average Score: 84.0
    Scores:        84.0
    Win Rate:      0/1 (0.00)
    Record:        Loss
    *** Finished running ExpectimaxAgent on smallClassic after 1 seconds.
    *** Won 0 out of 1 games. Average score: 84.000000 ***
    *** PASS: test_cases\q4\7-pacman-game.test

    ### Question q4: 5/5 ###


    Finished at 13:32:05

    Provisional grades
    ==================
    Question q4: 5/5
    ------------------
    Total: 5/5

    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, agentIndex, depth):

            # Terminal condition
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            actions = state.getLegalActions(agentIndex)

            if len(actions) == 0:
                return self.evaluationFunction(state)

            # PACMAN (MAX)
            if agentIndex == 0:
                value = float('-inf')
                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, expectimax(successor, nextAgent, nextDepth))
                return value

            # GHOST (EXPECTATION)
            else:
                value = 0
                prob = 1.0 / len(actions)

                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value += prob * expectimax(successor, nextAgent, nextDepth)

                return value

        # Root decision
        bestAction = None
        bestValue = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = expectimax(successor, 1, 0)

            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction
        util.raiseNotDefined()
