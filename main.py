import numpy as np
from queue import Queue


class solver:
    def __init__(self, grid):
        self.grid = grid
    def isValidPercolation(self, grid, diagonals = True):  
        rows, columns = len(grid), len(grid[0])
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),        
                (1, 1), (-1, 1), (-1, -1), (1, -1)]
        if diagonals == False:
            dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = Queue()
        visited = set()

        # Add all top-row starts
        for column in range(columns):
            if grid[0][column] == 1:
                queue.put((0, column))
                visited.add((0, column))

        if queue.empty():
            return False
        while not queue.empty():
            x, y = queue.get()

            if x == rows - 1:
                return True

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < rows and
                    0 <= ny < columns and
                    grid[nx][ny] == 1 and
                    (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.put((nx, ny))

        return False

    def calculateChance(self, simulationNum):
        validGrids = 0
        trials = 0
        while trials < simulationNum:
            trials += 1
            randomGrid = self.grid.randomiseGrid()
            if self.isValidPercolation(randomGrid) == True:
                validGrids += 1
        return validGrids/simulationNum * 100

class percolationGrid:
   def __init__(self, size):
      self.grid = []
      self.size = size 
      columns = 0
      while columns < size:
         row = []
         rows = 0
         while rows < size:
            row.append(0)
            rows += 1
         self.grid.append(row)
         columns += 1
   def returnGrid(self):
      return self.grid
   def setPoint(self, x, y):
        self.grid[x][y] = 1
   def randomiseGrid(self):
        randomGrid = []
        for i in range(self.size):
            randomRow = []
            for j in range(self.size):
                if self.grid[i][j] == 1:
                    randomValue = np.random.randint(2)
                else:
                    randomValue = 0
                randomRow.append(randomValue)
            randomGrid.append(randomRow)
        return randomGrid

test = percolationGrid(2)
test.setPoint(0,0)
test.setPoint(1,0)
examplePercolate = solver(test) 
print("Orignal")
print(test.returnGrid())
print("Original")
print(examplePercolate.calculateChance(50000))


