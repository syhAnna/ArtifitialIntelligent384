# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
	"""
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

	def getStartState(self):
		"""
        Returns the start state for the search problem.
        """
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
	"""
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
	# get the start state, stored as ([currentPath], [moves])
	start = ([problem.getStartState()], [])
	# choose Stack data structure for the DFS
	open_set = util.Stack()
	open_set.push(start)

	while not open_set.isEmpty():
		curr_path, curr_moves = open_set.pop()
		curr_state = curr_path[len(curr_path) - 1]
		if problem.isGoalState(curr_state):
			return curr_moves
		for successor, action, cost in problem.getSuccessors(curr_state):
			if successor not in curr_path:
				open_set.push((curr_path + [successor], curr_moves + [action]))
	return []


def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	# get the start state, stored as ([currentPath], [moves])
	start = ([problem.getStartState()], [])
	seen = {problem.getStartState(): 0}
	# choose Stack data structure for the BFS
	open_set = util.Queue()
	open_set.push(start)

	while not open_set.isEmpty():
		curr_path, curr_moves = open_set.pop()
		curr_state = curr_path[len(curr_path) - 1]

		if problem.getCostOfActions(curr_moves) <= seen[curr_state]:
			if problem.isGoalState(curr_state):
				return curr_moves
			for successor, action, cost in problem.getSuccessors(curr_state):
				if (successor not in seen.keys()) \
						or (problem.getCostOfActions(curr_moves + [action])
						    < seen[successor]):
					seen[successor] = problem.getCostOfActions(
						curr_moves + [action])
					open_set.push(
						(curr_path + [successor], curr_moves + [action]))
	return []


def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	# get the start state, stored as ([currentPath], [moves])
	start = ([problem.getStartState()], [])
	seen = {problem.getStartState(): 0}
	# choose Stack data structure for the UCS
	open_set = util.PriorityQueue()
	open_set.push(start, 0)

	while not open_set.isEmpty():
		curr_path, curr_moves = open_set.pop()
		curr_state = curr_path[len(curr_path) - 1]
		if problem.getCostOfActions(curr_moves) <= seen[curr_state]:
			if problem.isGoalState(curr_state):
				return curr_moves
			for successor, action, cost in problem.getSuccessors(curr_state):
				if (successor not in seen.keys()) or (problem.getCostOfActions(
						curr_moves + [action]) < seen[successor]):
					seen[successor] = problem.getCostOfActions(
						curr_moves + [action])
					open_set.update((curr_path + [successor],
					                 curr_moves + [action]), seen[successor])
	return []


def nullHeuristic(state, problem=None):
	"""
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
	return 0


def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	# get the start state, stored as (currentPath, moves)
	start = ([problem.getStartState()], [])
	seen = {problem.getStartState(): 0}
	# choose Stack data structure for the A*
	open_set = util.PriorityQueue()
	# to break tie: the same f, we want state with less heuristic function
	# store item as: [([currPath], [moves]), h(currState), f(currState)]
	open_set.push([start, heuristic(problem.getStartState(), problem),
	               0 + heuristic(problem.getStartState(), problem)],
	              0 + heuristic(problem.getStartState(), problem))

	while not open_set.isEmpty():
		curr_item = open_set.pop()

		# Break tie part:
		# priority queue with heristic value as priority, tie queue
		# with the same f-value
		candidate = util.PriorityQueue()
		candidate.push(curr_item, curr_item[1])
		while not open_set.isEmpty():
			potential = open_set.pop()
			if potential[2] == curr_item[2]:
				candidate.push(potential, potential[1])
			else:
				open_set.push(potential, potential[2])
				break
		curr_item = candidate.pop()
		# push remaining items back to open set
		while not candidate.isEmpty():
			pushBack = candidate.pop()
			open_set.push(pushBack, pushBack[2])
		curr = curr_item[0]
		curr_path, curr_moves = curr

		# A* algorithm part:
		curr_state = curr_path[len(curr_path) - 1]
		if problem.getCostOfActions(curr_moves) <= seen[curr_state]:
			if problem.isGoalState(curr_state):
				return curr_moves
			for successor, action, cost in problem.getSuccessors(curr_state):
				if (successor not in seen.keys()) or (problem.getCostOfActions(
						curr_moves + [action]) < seen[successor]):
					seen[successor] = problem.getCostOfActions(
						curr_moves + [action])
					open_set.update([(curr_path + [successor], curr_moves + [action]),
					                 heuristic(successor, problem),
					                 seen[successor] + heuristic(successor, problem)],
					                seen[successor] + heuristic(successor, problem))
	return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
