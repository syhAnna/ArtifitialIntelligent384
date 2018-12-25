def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      We considered two aspects: the position of food and the postion of ghosts.
      And we use the built-in getScore function as basic evaluation.
      Additionally we add some extra criteria including the reciprocal of the min-distance between pacman and food, and ghosts.
    """

    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    currentGhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

    def food_score_func(gameState):
        min_dist = 1e6
        if len(gameState.getFood().asList()) == 0:
            return 0
        for food in gameState.getFood().asList():
            dist = manhattanDistance(gameState.getPacmanPosition(), food)
            if dist < min_dist:
                min_dist = dist
        return 1.0 / min_dist

    def ghost_score_func(gameState):
        score = 0
        for ghost in gameState.getGhostStates():
            dist = manhattanDistance(
                gameState.getPacmanPosition(), ghost.getPosition())
            if ghost.scaredTimer > 0:
                score += max(8 - dist, 0)
            else:
                score -= max(7 - dist, 0)
        return score

    def capsule_score_func(gameState):
        if len(gameState.getCapsules()) == 0:
            return 0
        min_dist = 1e6
        for capsule in gameState.getCapsules():
            dist = manhattanDistance(gameState.getPacmanPosition(), capsule)
            if dist < min_dist:
                min_dist = dist
        return 1.0 / min_dist

    g_score = ghost_score_func(currentGameState)
    f_score = food_score_func(currentGameState)
    c_score = capsule_score_func(currentGameState)
    base_score = currentGameState.getScore()
    return g_score * (abs(g_score)) + f_score + (50 * c_score) + base_score


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currentPosition = currentGameState.getPacmanPosition()

    foods = currentGameState.getFood().asList()
    foodDistances = [manhattanDistance(f, currentPosition) for f in foods]
    minFood = min(foodDistances) if foodDistances else 0
    avgDistance = sum(foodDistances) / len(foodDistances) if foodDistances else 0

    ghosts = currentGameState.getGhostPositions()
    ghostDistances = [manhattanDistance(g, currentPosition) for g in ghosts]
    minGhost = min(ghostDistances) if ghostDistances else 0

    capsules = currentGameState.getCapsules()
    capsulesDistances = [manhattanDistance(c, currentPosition) for c in capsules]
    minCapsules = min(capsulesDistances) if capsulesDistances else 0

    score = - (1000 * len(foods) + 800 * len(capsules) + 100 * minFood + 10 * avgDistance ) + 10 * minGhost  + 100 * currentGameState.getScore()

    if len(foods) == 1:
        score = - (100 * manhattanDistance(foods[0], currentPosition) + 10 * avgDistance) + 10 * minGhost + 100 * currentGameState.getScore()

    # score += random.randint(1, 80)

    if currentGameState.isWin():
        score = 99999999
    if currentGameState.isLose():
        score = - 99999999

    return score + random.randint(1, 80)
