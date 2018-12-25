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
    def disFeature(pacman, featuresList):
        featuresDistance = [manhattanDistance(pacman, feature) for feature in
                          featuresList]
        if len(featuresDistance) != 0:
            return min(featuresDistance), float(sum(featuresList)) / float(len(featuresList))
        else:
            return 0, 0

    # Current Pacman position
    pacmanPos = currentGameState.getPacmanPosition()
    # The game score
    origScore = currentGameState.getScore()

    # Get the position of the 3 important features
    ghostsPositions = currentGameState.getGhostPositions()
    capsulesPositions = currentGameState.getCapsules()
    foodsPositions = currentGameState.getFood().asList()

    # Distance to the nearest feature, average distance of each feature
    disNearGhost, averageGhosts = disFeature(pacmanPos, ghostsPositions)[0], disFeature(pacmanPos, ghostsPositions)[1]
    disNearCapsule, averageCapsules = disFeature(pacmanPos, capsulesPositions)[0], disFeature(pacmanPos, capsulesPositions)[1]
    disNearFood, averageFoods = disFeature(pacmanPos, foodsPositions)[0], disFeature(pacmanPos, foodsPositions)[1]

    # Can consider ghost scare time, eat ghost first, this add score
    # Need to give appropriate weight to linear combine each feature
