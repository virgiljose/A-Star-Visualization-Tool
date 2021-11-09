import math
import pygame
from queue import PriorityQueue

LENGTH = 1000
WIN = pygame.display.set_mode((LENGTH, LENGTH))
pygame.display.set_caption("A* Algorithm Visualization")

# Constants respresenting states of Node as a color
CLOSED = (255,0,0) # Red
OPEN = (0,255,0) # Green
DEFAULT = (255,255,255) # White
START = (255,128,0) # Orange
END = (0,0,255) # Blue
PATH = (191,0,255) # Violet
WALL = (0,0,0) # Black
GRID_LINE = (128,128,128) # Grey

# Stores information about the position and state of each node
class Node:

    def __init__(self, pos, cell_size):

        # Position in grid
        self.row = pos[0]
        self.col = pos[1]

        # Position on screen
        self.screen_x = pos[0] * cell_size
        self.screen_y = pos[1] * cell_size

        self.cell_size = cell_size

        # State of Node
        self.state = DEFAULT
    
    def get_pos(self):
        return (self.row, self.col)
    
    def draw_cell(self, win):
	    pygame.draw.rect(win, self.state, (self.screen_x, self.screen_y, self.cell_size, self.cell_size))

    # FUNCTIONS THAT CHECK CURRENT STATE OF NODE
    def is_closed(self):
        return self.state == CLOSED
    
    def is_open(self):
        return self.state == OPEN
    
    def is_start(self):
        return self.state == START
    
    def is_end(self):
        return self.state == END

    def is_wall(self):
        return self.state == WALL

    # FUNCTIONS THAT SET NEW STATE FOR NODE
    def set_closed(self):
        self.state = CLOSED

    def set_open(self):
        self.state = OPEN

    def set_start(self):
        self.state = START
    
    def set_end(self):
        self.state = END

    def set_wall(self):
        self.state = WALL
    
    def set_default(self):
        self.state = DEFAULT
    
    def set_path(self):
        self.state = PATH


def reconstruct_path(prev, curr):
    while curr in prev:
        curr = prev[curr][0]
        curr.set_path()
    return True

# Heuristic function / also used to calculate dist from curr to neighbor
# curr: current node
# end: end node
def dist(curr, end):
    # Calculate Euclidian distance from curr to end
    # curr = (x coord of curr, y coord of curr)
    # end = (x coord of end, y coord of end)
    curr_row, curr_col = curr.get_pos()
    end_row, end_col = end.get_pos()
    return math.sqrt(((end_row - curr_row) ** 2) + ((end_col - curr_col) ** 2))

# start and end are Node objects
# grid is a 2-d list of Nodes
def a_star(draw, start, end, grid):
    
    # Set of discovered nodes
    # count used as a tie-breaker if two nodes have same f-score. Earliest node discovered first
    # Format: (f_score[node], count, node)
    open_set = PriorityQueue()
    open_set_hash = {start}
    count = 0

    # For a given node n, prev[n] is a tuple:
    # first element: the node immediately preceding it on the currently known cheapest path from start to n
    # second element: whether we have already traversed a wall
    # Format: { n1: (prev_n1, traversed_wall), ... }
    prev = {}

    # For a given node n: g_score[n] is the cost of the cheapest known
    # path from start to n
    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start] = 0

    # For a given node n: f_score[n] = g_score[n] + h(n)
    # Approximation of cost from start to end through n
    f_score = {cell: float('inf') for row in grid for cell in row}
    f_score[start] = dist(start, end)

    open_set.put((f_score[start], count, start))

    while open_set:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the node in open_set with the lowest f_score value
        curr = open_set.get()[2]
        open_set_hash.remove(curr)

        # If we have reached the end, we are done searching for paths.
        # Reconstruct the path.
        if curr == end:
            return reconstruct_path(prev, curr)
        
        # Look at each neighbor of curr:
        curr_x, curr_y = curr.get_pos()
        for i in [(x,y) for x in range(-1,2) for y in range(-1,2) if x != 0 or y != 0]:
            # Check if the coordinates are out of bounds
            new_x, new_y = curr_x + i[0], curr_y + i[1]
            if new_x < 0 or new_x >= len(grid) or new_y < 0 or new_y >= len(grid):
                continue
            neighbor = grid[new_x][new_y]
            #print("neighbor of {}: {}".format(curr.get_pos(), neighbor.get_pos()))

            # Check whether the neighbor is a wall and whether we have already traversed a wall on the current path:
            traversed_wall = False
            if prev and curr in prev:
                traversed_wall = prev[curr][1]
            if traversed_wall and neighbor.is_wall():
                continue

            tentative_g_score = g_score[curr] + dist(curr, neighbor)
            if tentative_g_score < g_score[neighbor]:
                prev[neighbor] = (curr, traversed_wall or neighbor.is_wall())
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + dist(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_wall():
                        neighbor.set_open()
        
        draw()

        if curr != start and not curr.is_wall():
            curr.set_closed()
    
    return False

def generate_grid(rows, length):
    grid = []
    cell_size = length // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node((i,j), cell_size))
    return grid

def draw(win, grid, rows, length):
    win.fill(DEFAULT)

    for row in grid:
        for cell in row:
            cell.draw_cell(win)
    
    cell_size = length // rows
    for i in range(rows):
        pygame.draw.line(win, GRID_LINE, (0, i * cell_size), (length, i * cell_size))
    for j in range(rows):
        pygame.draw.line(win, GRID_LINE, (j * cell_size, 0), (j * cell_size, length))
    
    pygame.display.update()

def get_mouse_pos(pos, rows, length):
    cell_size = length // rows
    y, x = pos

    row = y // cell_size
    col = x // cell_size

    return (row, col)

def main():

    ROWS = 50
    grid = generate_grid(ROWS, LENGTH)

    start, end = None, None

    run = True # Flag indicating whether game should run (sets to false when player presses quit)
    while run:
        draw(WIN, grid, ROWS, LENGTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            # Left button clicks: set cells
            if pygame.mouse.get_pressed()[0]: # Left button clicked
                pos = pygame.mouse.get_pos() # Get coordinates of mouse on screen
                row, col = get_mouse_pos(pos, ROWS, LENGTH) # Convert to row/col position in grid
                cell = grid[row][col] # Find the corresponding cell in grid
               
                if not start and cell != end:
                    start = cell
                    start.set_start()
                elif not end and cell != start:
                    end = cell
                    cell.set_end()
                elif cell != end and cell != start:
                    cell.set_wall()
            
            # Right button clicks: reset cells
            elif pygame.mouse.get_pressed()[2]: # Right button clicked
                pos = pygame.mouse.get_pos() # Get coordinates of mouse on screen
                row, col = get_mouse_pos(pos, ROWS, LENGTH) # Convert to row/col position in grid
                cell = grid[row][col] # Find the corresponding cell in grid
                cell.set_default()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    a_star(lambda: draw(WIN, grid, ROWS, LENGTH), start, end, grid)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = generate_grid(ROWS, LENGTH)
    
    pygame.quit()


if __name__ == '__main__':
    main()