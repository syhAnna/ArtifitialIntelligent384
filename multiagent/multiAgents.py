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
		# during the scared time, pacmen can reach the ghost

		"*** YOUR CODE HERE ***"
		score, near_food, near_ghost = 0, 0, 0

		# Foods part
		if len(newFood.asList()) != 0:
			near_food = min([manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()])
			score -= near_food
		# Increment score if next state has food
		if newPos in currentGameState.getFood().asList():
			score += near_food

		# Ghost part
		if len(newGhostStates) != 0:
			near_ghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
			# During scare time can touch ghost
			flag = True
			for scare in newScaredTimes:
				if scare != 0:
					flag = False
			if flag and near_ghost < 3:
				score = -1000000

		return score

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
		"""
		"*** YOUR CODE HERE ***"
		def DFMiniMax(state, agentIndex, depth):
			"""
			DFMiniMax search algorithm, with given depth.
			For example, if depth == 2, [Pacman and ALL ghosts] get 2 moves.
			Return best move for player(pos), and MAX's value for pos.
			"""
			best_move = None

			# base case
			if (depth == 0) and (agentIndex == 0):
				return best_move, self.evaluationFunction(state)

			# Check termination after each success group of move
			if agentIndex == state.getNumAgents():
				if (state.isWin()) or (state.isLose()):
					return best_move, self.evaluationFunction(state)
				else:
					return DFMiniMax(state, 0, depth - 1)

			# Initial value for MAX and MIN node
			if agentIndex == 0:
				value = -float("inf")
			else:
				value = float("inf")

			# the leaf is non-terminal node
			if len(state.getLegalActions(agentIndex)) == 0:
				return best_move, self.evaluationFunction(state)

			# Loop through each valid action, recursion
			for move in state.getLegalActions(agentIndex):
				nxt_state = state.generateSuccessor(agentIndex, move)
				nxt_move, nxt_val = DFMiniMax(nxt_state, agentIndex + 1, depth)
				if agentIndex == 0 and value < nxt_val:
					value, best_move = nxt_val, move
				if agentIndex > 0 and value > nxt_val:
					value, best_move = nxt_val, move

			return best_move, value

		return DFMiniMax(gameState, 0, self.depth)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		def AlphaBeta(state, agentIndex, depth, alpha, beta):
			"""
			The Alpha-Beta Pruning algorithm.
			Return best move for player(pos), and MAX's value for pos.
			"""
			best_move = None

			# base case
			if (depth == 0) and (agentIndex == 0):
				return best_move, self.evaluationFunction(state)

			# Check termination after each success group of move
			if agentIndex == state.getNumAgents():
				if (state.isWin()) or (state.isLose()):
					return best_move, self.evaluationFunction(state)
				else:
					return AlphaBeta(state, 0, depth - 1, alpha, beta)

			# Initial value for MAX and MIN node
			if agentIndex == 0:
				value = -float("inf")
			else:
				value = float("inf")

			# the leaf is non-terminal node
			if len(state.getLegalActions(agentIndex)) == 0:
				return best_move, self.evaluationFunction(state)

			# Loop through each valid action, recursion
			for move in state.getLegalActions(agentIndex):
				nxt_state = state.generateSuccessor(agentIndex, move)
				nxt_move, nxt_val = AlphaBeta(nxt_state, agentIndex + 1, depth, alpha, beta)
				if agentIndex == 0:
					if value < nxt_val:
						value, best_move = nxt_val, move
					if value >= beta:
						return best_move, value
					alpha = max(alpha, value)
				if agentIndex > 0:
					if value > nxt_val:
						value, best_move = nxt_val, move
					if value <= alpha:
						return best_move, value
					beta = min(beta, value)

			return best_move, value

		return AlphaBeta(gameState, 0, self.depth, -float("inf"), float("inf"))[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		"*** YOUR CODE HERE ***"
		def Expectimax(state, agentIndex, depth):
			"""
			Expectimax search algorithm, with given depth.
			Return best move for player(pos), and MAX's value for pos.
			"""
			best_move = None

			# base case
			if (depth == 0) and (agentIndex == 0):
				return best_move, self.evaluationFunction(state)

			# Check termination after each success group of move
			if agentIndex == state.getNumAgents():
				if (state.isWin()) or (state.isLose()):
					return best_move, self.evaluationFunction(state)
				else:
					return Expectimax(state, 0, depth - 1)

			# Initial value for MAX and MIN node
			if agentIndex == 0:
				value = -float("inf")
			else:
				value = 0

			# the leaf is non-terminal node
			if len(state.getLegalActions(agentIndex)) == 0:
				return best_move, self.evaluationFunction(state)

			# Loop through each valid action, recursion
			for move in state.getLegalActions(agentIndex):
				nxt_state = state.generateSuccessor(agentIndex, move)
				nxt_move, nxt_val = Expectimax(nxt_state, agentIndex + 1, depth)
				if agentIndex == 0 and value < nxt_val:
					value, best_move = nxt_val, move
				if agentIndex > 0:
					value += (1.0 / float(len(state.getLegalActions(agentIndex)))) * nxt_val

			return best_move, value

		return Expectimax(gameState, 0, self.depth)[0]


def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	  [pick the action with higher score]
	  - Important features to be considered:
		Ghosts, Capsules (larger dot, send ghost back and has scare), Foods.
	  - Consider the manhattan distance between the CURRENT Pacman state to
		these important features.
	  - Use a linear combination of these features. According to importance
		give each feature different 'weight' in the linear combination.
	"""
	"*** YOUR CODE HERE ***"
	# get the data of current game state
	pacmanPos = currentGameState.getPacmanPosition()
	currScore = currentGameState.getScore()

	# Important features: capsules, foods, ghosts, consider scare time
	capsulesPositions = currentGameState.getCapsules()
	foodsPositions = currentGameState.getFood().asList()
	ghostsStates = currentGameState.getGhostStates()

	def min_distance(pos1, listPos2):
		"""
		Return the minimum distance of pos1 and pos2 in listPos2.
		"""
		minDistance = 0
		if len(capsulesPositions) != 0:
			minDistance = min(
				[manhattanDistance(pos1, pos2) for pos2 in listPos2])
		return minDistance

	# case1: [++capsules, +foods], -ghosts
	# case2: (during the scare time) +++Sghosts, [++capsules, +foods], -ghosts

	capsuleMinDistance = min_distance(pacmanPos, capsulesPositions)
	foodMinDistance = min_distance(pacmanPos, foodsPositions)
	capsuleScore, foodScore, ghostScore = 0, 0, 0

	if capsuleMinDistance != 0:
		capsuleScore = 1.0 / capsuleMinDistance
	if foodMinDistance != 0:
		foodScore = 1.0 / foodMinDistance

	# Ghost part, consider whether the ghost is in the scare time
	for ghost in ghostsStates:
		ghostDistance = manhattanDistance(pacmanPos, ghost.getPosition())
		if ghost.scaredTimer > 0:
			ghostScore += (8 - ghostDistance) if (8 - ghostDistance > 0) else 0
		else:
			ghostScore -= (7 - ghostDistance) if (7 - ghostDistance > 0) else 0
	return currScore + 45 * capsuleScore + foodScore + ghostScore * abs(ghostScore)


# Abbreviation
better = betterEvaluationFunction
