# This program is creating a template for a monte carlo tree

# Things that includes:

# - game states, i.e. the nodes of the tree
# - the tree itself

import random
import numpy as np


# Things a game state needs:
# - the literal game state (board)
# - pointer to the parent (if it exists)
# - pointers to the children (if they exist)
# - a total score
# - a counter to keep track of the number of visits
# - a method to calculate UCBI

# note: what is UCBI? It's a way to balance between exploration and exploitation.
# Exploitation side is the average value (self.total/self.visits)
# Exploration side is 2 * √(ln(visits to parent)/visits to child)
# UCBI is sum of Exploitation value + Exploration value
class GameState:

    def __init__(self, board):
        self.board = board
        self.total = 0
        self.visits = 0

        self.parent = None
        self.children = []

    def setParent(self, parentState):
        self.parent = parentState
        parentState.addChild(self)

    def addChild(self, childState):
        self.children.append(childState)

    def addToTotal(self, newValue):
        self.total += newValue

        # now we have to update the parent as well
        # to do this, we'll use a bit of recursion!

        # base case:
        if self.parent == None:
            return
        # recursive step:
        else:
            self.parent.addToTotal(newValue)

    def addVisit(self):
        self.visits += 1

        # same as above
        # base case:
        if self.parent == None:
            return
        # recursive step:
        else:
            self.parent.addVisit()

    def calculateUCBI(self):
        # Formula:
        # average value + 2*√(ln(visits to parent)/visits to child)

        # THINGS THAT CAN BE 0
        # - self.visits -> return infinity because we have a fully unexplored branch
        # - self.parent -> CANNOT BE NONE because then this would never get called!
        # - self.total -> doesn't cause 0 division errors so we don't care

        if self.visits == 0:
            return np.Infinity

        else:
            exploitationValue = self.total / self.visits

            # NOTE: np.log is actually ln(), np.log10 is standard log()
            explorationValue = 2 * np.sqrt(np.log(self.parent.visits)/self.visits)

            return exploitationValue + explorationValue

    def getChildrenUCBIs(self):
        childScores = []

        for child in self.children:
            childScores.append(child.calculateUCBI())

        return childScores

S0 = GameState(None)
S1 = GameState(None)
S2 = GameState(None)

S1.setParent(S0)
S2.setParent(S0)

S1.addToTotal(20)
S1.addVisit()
print(S0.getChildrenUCBIs())


S2.addToTotal(10)
S2.addVisit()
print(S0.getChildrenUCBIs())

S3 = GameState(None)
S3.setParent(S1)
S3.addToTotal(0)
S3.addVisit()

print(S0.getChildrenUCBIs())
