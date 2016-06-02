import sys
import math
import heapq
import time
import random

class Problem:
    def __init__(self, board):
        self.variables = []
        self.board = board[:]

        for c in range(0, 9):
            for r in range(0, 9):
                if self.board[r][c] == 0:
                    self.variables.append((r, c, range(1, 10)))

    def getAllAssociatedVariables(self, var):
        allAssociatedVariables = []
        for variable in self.variables:
            if self.inRow(var, variable) or self.inCol(var, variable) or self.inBox(var, variable):
                allAssociatedVariables.append(variable)
        return allAssociatedVariables

    def inRow(self, var1, var2):
        return var1[0] == var2[0]

    def inCol(self, var1, var2):
        return var1[1] == var2[1]

    def inBox(self, var1, var2):
        return var1[0]//3 == var2[0]//3 and var1[1]//3 == var2[1]//3

    def getMostRestrictedVariables(self):
        variables = sorted(self.variables, key=lambda variable: variable[-1])
        return [variable for variable in variables if len(variable[2]) == len(variables[0][2])]

    def getLeastConstrainingValue(self, variable):
        allAssociatedVariables = self.getAllAssociatedVariables(variable)

        leastConstrainingValue = 0
        leastConstrainingScore = 999
        for value in variable[2]:
            score = 0
            for associatedVariables in allAssociatedVariables:
                if value in associatedVariables[2]:
                    score += 1
            if score < leastConstrainingScore:
                leastConstrainingScore = score
                leastConstrainingValue = value

        return leastConstrainingValue

    def getMostConstrainingVariables(self, variables):
        mostConstrainingVariables = []
        mostConstrainingSize = 999
        for variable in variables:
            allAssociatedVariables = self.getAllAssociatedVariables(variable)
            if mostConstrainingSize > len(allAssociatedVariables):
                mostConstrainingSize = len(allAssociatedVariables)
                mostConstrainingVariables.append(variable)
        return mostConstrainingVariables

    def setValue(self, value, variable):
        self.board[variable[0]][variable[1]] = value
        self.variables.remove(variable)
        for variable in self.variables:
            if value in variable[2]:
                variable[2].remove(value)

    def undoValueSet(self, value, variable):
        self.board[variable[0]][variable[1]] = 0
        self.variables.append(variable)
        for variable in self.variables:
            variable[2].append(value)

    def isComplete(self):
        for c in range(0, 9):
            for r in range(0, 9):
                if self.board[r][c] == 0:
                    return False
        return True
        
def solve(problem):
    if problem.isComplete():
        return problem

    mostRestrictedVariables = problem.getMostRestrictedVariables()

    mostConstrainingVariables = problem.getMostConstrainingVariables(mostRestrictedVariables);

    for mostConstrainingVariable in mostConstrainingVariables:
        leastConstrainingValue = problem.getLeastConstrainingValue(mostConstrainingVariable)

        problem.setValue(leastConstrainingValue, mostConstrainingVariable)

        if solve(problem):
            return problem
        else:
            problem.undoValueSet(leastConstrainingValue, mostConstrainingVariable)

    return False

# Reading from stdin
board = []

for line in sys.stdin:
    parsedInput = line.split(' ')
    if len(parsedInput) > 1:
        board.append([int(parsedInput[c]) for c in range(0, 9)])

sudoku = Problem(board)
solve(sudoku)

print board
