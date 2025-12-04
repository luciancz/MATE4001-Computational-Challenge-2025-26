import numpy as np
from queue import Queue
import matplotlib.pyplot as plt


class solver:
    def __init__(self, grid):
        self.grid = grid
    def isValidPercolation(self, grid, diagonals, periodic):
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
            x, y = queue.get() # Deque

            if x == rows - 1:
                return True # checks if you are on the last row

            for dx, dy in dirs: # checking all different permutations of directions, if it is valid it adds it back to the queue
                nx, ny = x + dx, y + dy
                if (periodic == True):
                    ny = (y + dy) % columns

                if ( 0 <= nx < rows and 0 <= ny < columns and grid[nx][ny] == 1 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.put((nx, ny))

        return False

    def calculateChance(self, simulationNum, p, diagonals = True, periodic = True): # Runs through the grid many times and calculates the probability
        validGrids = 0
        trials = 0
        while trials < simulationNum:
            trials += 1
            randomGrid = self.grid.randomiseGrid(p)
            if self.isValidPercolation(randomGrid, diagonals, periodic) == True:
                validGrids += 1
        #print("Valid: " + str(validGrids))
        #print("Trials: " + str(trials))
        return validGrids/simulationNum * 100

class percolationGrid: # class to create and manage underlying grid
   def __init__(self, size): # constructor function takes in size of Grid
      self.grid = [] #Initialise empty grid
      self.size = size
      columns = 0
      while columns < size: #appends columns
         row = []
         rows = 0
         while rows < size: # appends rows to columns
            row.append(0)
            rows += 1
         self.grid.append(row)
         columns += 1
   def returnGrid(self):
        return self.grid
   def setPoint(self, x, y): # manually activates a cell
        self.grid[x][y] = 1 # sets it to 1
   def randomiseGrid(self,p): # creates a new random grid of the same size
        return np.random.choice([0, 1], size=(self.size, self.size), p=[1-p, p]) # returns a NumPy 2D array

def plotSystemState(): # shows one random grid as an image
    gridSize = 10 # grid size 10x10
    prob = 0.6 # each cell active with this probability 
    
    # Generate data
    systemGrid = percolationGrid(gridSize)
    randomGrid = systemGrid.randomiseGrid(prob) 
    # Plot data as points on grid and draw as an image
    plt.figure(figsize=(10, 10)) 
    plt.imshow(randomGrid, cmap='viridis', interpolation='nearest') # interpolation = "nearest" means no smoothing
    plt.title("State of system when L=10 and p=0.6")
    plt.xlabel("")
    plt.ylabel("")
    print("Plot 1")
    plt.show()

# plotting how often the system percolates (fraction) as p varies from 0 to 1, under 4 conditions
def plotFractionActSystem():
    gridSize = 50
    simulationNum = 100 # Higher number = smoother curve
    probabilities = np.linspace(0, 1, 20) # probabilities is 20 equally spaced values between 0 and 1
    
    graphs = [
        (True, True, "Diagonals Allowed and Periodic Boundaries"), 
        (True, False, "Diagonals Allowed and Fixed Boundaries"), 
        (False, True, "Diagonals Not Allowed and Periodic Boundaries"),
        (False, False, "Diagonals Not Allowed and Fixed Boundaries")

    ]

    plt.figure(figsize=(10, 10))
    
    for diagonals, periodic, label in graphs:
        graphValues = []
        systemGrid = percolationGrid(gridSize)
        curSolver = solver(systemGrid)
        
        for p in probabilities:
            f = curSolver.calculateChance(simulationNum, p, diagonals, periodic) / 100 #convert probability to fraction
            graphValues.append(f)
            
        plt.plot(probabilities, graphValues, marker='x', linewidth=3, label=label)

    # creating a grid and solver for each configuration, calculating fraction that percolates and plotting it
    plt.xlabel("single-site activation probability", fontsize=11)
    plt.ylabel("fraction of activated systems ", fontsize=11)
    plt.title("fraction of activated systems vs single-site activation probability (L=50)", fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    print("Plot 2")
    plt.show()
def plotVariance(): #shows how variance changes with grid size
    # from 10 to 100 step size 5
    sizes = range(5, 101, 10) 
    graphProbabilities = [0.25, 0.6]
    # taking 100 measurements for each size, each measurement averaging 10 simulations 
    measurements = 100  
    simsPerMeasurement = 10 

    fig, axes = plt.subplots(1, 2, figsize=(15, 5)) 

    for i, p in enumerate(graphProbabilities): 
        variances = [] 
        for L in sizes:
            fList = [] # collecting a list of 100 fraction values
            systemGrid = percolationGrid(L) 
            curSolver = solver(systemGrid)
            for g in range(measurements):
                percentage = curSolver.calculateChance(simsPerMeasurement, p)
                f = percentage / 100.0
                fList.append(f)
            
            variances.append(np.var(fList)) # computing the variance from those 100 fraction values and appending to the list

        axes[i].plot(sizes, variances, marker='o', linewidth=2, color='red')
        axes[i].set_xlabel("Lattice Size", fontsize=12)
        axes[i].set_ylabel("Variance", fontsize=12)
        axes[i].set_title(f"Variance for (p={p})", fontsize=14)
        axes[i].grid(True)

    plt.tight_layout()
    print("Plot 3")
    plt.show()

# runs the three plotting functions
if __name__ == "__main__":
    plotSystemState()
    plotFractionActSystem()
    plotVariance()
