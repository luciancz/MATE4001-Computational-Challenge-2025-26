import numpy as np
from queue import Queue
import matplotlib.pyplot as plt


class solver:
    def __init__(self, grid):
        self.grid = grid
    def isValidPercolation(self, grid, diagonals = True): 
        rows, columns = len(grid), len(grid[0])
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),        
                (1, 1), (-1, 1), (-1, -1), (1, -1)] # directions if diagonals are not disabled
        if diagonals == False:
            dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)] # directions if diagonals are disabled 
        queue = Queue() # FIFO data structure (first thing coming in a queue is the first that comes out)
        visited = set() # keeps track of visited nodes

        # Add all top-row starts
        for column in range(columns): # checking points one by one 
            if grid[0][column] == 1:
                queue.put((0, column))
                visited.add((0, column)) # adding points in the top row to the queue 

        if queue.empty(): 
            return False # no points are valid
        while not queue.empty(): 
            x, y = queue.get() # Dequeue

            if x == rows - 1:
                return True # checks if you are on the last row

            for dx, dy in dirs: # checking all different permutations of directions, if it is valid it adds it back to the queue
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

    def calculateChance(self, simulationNum, p, diagonals = True): # Runs through the grid many times and calculates the probability
        validGrids = 0
        trials = 0
        while trials < simulationNum:
            trials += 1
            randomGrid = self.grid.randomiseGrid(p)
            if self.isValidPercolation(randomGrid, diagonals) == True:
                validGrids += 1
        #print("Valid: " + str(validGrids))
        #print("Trials: " + str(trials))
        return validGrids/simulationNum * 100

class percolationGrid: # creating the grid
   def __init__(self, size): # constructive function
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
   def randomiseGrid(self,p):
        randomGrid = []
        for i in range(self.size):
            randomRow = []
            for j in range(self.size):
                randomValue = np.random.choice([0, 1], p=[1-p, p])
                randomRow.append(randomValue)
            randomGrid.append(randomRow)
        return randomGrid

test = percolationGrid(10) # size of the grid
prob = 0.6 # probability

examplePercolate = solver(test) 
#print("Orignal")
#print(test.returnGrid())
#print("Original")
#print(examplePercolate.calculateChance(500, prob))
#print("Done")
exampleRandomGrid = percolationGrid(10).randomiseGrid(prob)
plt.imshow(exampleRandomGrid, cmap='viridis', interpolation='nearest')
plt.title("Percolation Grid")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()




def plot_fraction_vs_p():
    L = 50
    simulationNum = 20
    probabilities = [0.25, 0.4, 0.6, 0.8]
    configs = [(True, simulationNum), (False, simulationNum)]
    labels = ["Diagonals=True", "Diagonals=False"]

    plt.figure(figsize=(10, 6))
    for (diagonals, sims), label in zip(configs, labels):
        f_values = []
        for p in probabilities:
            grid = percolationGrid(L)
            s = solver(grid)
            f = s.calculateChance(sims, p, diagonals)
            f_values.append(f)
        plt.plot(probabilities, f_values, marker='o', linewidth=2, label=label)

    plt.xlabel("Activation Probability p", fontsize=12)
    plt.ylabel("Fraction of Activated Systems f", fontsize=12)
    plt.title("Fraction f vs Activation Probability p (L=50)", fontsize=14)
    plt.xticks(probabilities)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def plot_variance_vs_L():
    sizes = range(10, 101, 10)
    simulationNum = 10
    probabilities = [0.25, 0.6]

    for p in probabilities:
        variances = []
        for L in sizes:
            f_values = []
            for _ in range(simulationNum):
                grid = percolationGrid(L)
                s = solver(grid)
                f_values.append(s.calculateChance(1, p))
            variances.append(np.var(f_values))

        plt.figure(figsize=(8, 5))
        plt.plot(sizes, variances, marker='o', linewidth=2)
        plt.xlabel("Lattice Size L", fontsize=12)
        plt.ylabel("Variance of f", fontsize=12)
        plt.title(f"Variance of f vs L for p={p}", fontsize=14)
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# Run the plots
plot_fraction_vs_p()
plot_variance_vs_L()


