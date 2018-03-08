import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

'''
This is a simple representation of John Conway's Game of Life which is a simplistic population model. The basic 
conditions are that a square with less than 2 or more than 3 neighbors (under or overpopulation, respectively) is 
considered 'dead,' and those with exactly 2 or 3 neighbors is 'alive.' A dead cell can become alive if it has exactly 3 
living neighbors.
'''

# Create dictionary of pre-set seeds
seed_list = {'blinker': [[0, 1, 0],
                         [0, 1, 0],
                         [0, 1, 0]],
             'beacon':  [[1, 1, 0, 0],
                         [1, 1, 0, 0],
                         [0, 0, 1, 1],
                         [0, 0, 1, 1]],
             'pulsar':  [[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                         [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                         [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                         [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                         [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                         [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                         [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]],
             'glider':  [[1, 0, 1],
                         [0, 1, 1],
                         [0, 1, 0]],
             'r-pentomino': [[0, 1, 1],
                             [1, 1, 0],
                             [0, 1, 0]],
             'spaceship': [[0, 1, 0, 0, 1],
                           [1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 1],
                           [1, 1, 1, 1, 0]],
             'L-pattern': [[1, 0],
                           [1, 0],
                           [1, 0],
                           [1, 1],
                           [1, 1]]
             }


# Find number of nearest neighbors to determine if cell lives or dies
def check_for_life(x, y):
    neighbors = np.sum(grid[x-1:x+2, y-1:y+2]) - grid[x, y]
    if grid[x, y] and not 2 <= neighbors <= 3:
        return 0
    elif neighbors == 3:
        return 1
    return grid[x, y]


# Create new generation based on previous grid and set as the new primary grid
def generations():
    global grid
    grid_update = np.copy(grid)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            grid_update[x, y] = check_for_life(x, y)

    grid = np.copy(grid_update)

# Accept user inputs to set conditions
status = True
while status:
    grid_size = int(input('Please input an integer of the grid size to display (nxn, recommend less than 100): '))
    num_gens = int(input('Please input how many generations you would like to see: '))
    try:
        seed = input('Please choose a seed from the list (blinker, beacon, pulsar, glider, r-pentomino, spaceship,'
                     ' L-pattern): ')
    except KeyError:
        print('Please type an exact seed from the list')
    x_start = int(input('Starting x position (integer between 0 and ' + str(grid_size) + ')?: '))
    y_start = int(input('Starting y position (integer between 0 and ' + str(grid_size) + ')?: '))
    grid = np.zeros((grid_size, grid_size))
    seed_format = np.array(seed_list[seed])
    try:
        grid[x_start:seed_format.shape[0]+x_start, y_start:seed_format.shape[1]+y_start] = seed_format
        status = False
    except ValueError:
        print("I'm sorry, please choose a larger grid size for this seed.")

# initializes figure with axes turned off
fig = plt.figure()
plt.axis('off')

# creates an empty list to store new grids and calls generations function to generate next grid
gens = []
for i in range(num_gens):
    title = plt.text(1, -1, 'Generation ' + str(i))
    gens.append((plt.imshow(grid, cmap='winter'), title,))
    generations()

# creates animation of generations
gens_animation = animation.ArtistAnimation(fig, gens, interval=200, blit=False)

# sets up the video writer and saves file to current project directory
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
writer = animation.FFMpegWriter(fps = 5, extra_args = ['-vcodec','libx264'])
gens_animation.save((str(seed) + '.mp4'), writer = writer)

# shows animation loop
plt.show()