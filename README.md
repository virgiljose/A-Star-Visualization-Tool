# A Star Visualization Tool
 
Modification of TechWithTim's A* Path Finding Visualization (https://github.com/techwithtim/A-Path-Finding-Visualization).

In this modification:
- The path is allowed to traverse through up to one wall
- The path can travel in eight directions instead of four
- Distance is calculated based on Euclidian distance, rather than Manhattan distance. Therefore, a neighboring diagonal cell is considered to be slightly farther than a neighboring orthogonal cell (e.g. a cell immediately above/below or to the left/right).

This visualization tool finds the shortest path from the selected start point to the selected end point, taking into account walls that may be blocking the path (up to one wall may be traversed through).

Usage:
1. Run the command: python3 ./a_star.py
2. Set cells to be the starting point, ending point, or a wall, by left-clicking a given cell:
    - If no starting point has been selected, left-clicking will make the selected cell a starting point
    - If a starting point has been selected, but no ending point has been selected, left-clicking will make the selected cell an ending point
    - Otherwise, left-clicking will make the cell a wall
3. Right-click a cell to reset the cell.

Cell colors:
- Orange: Start point
- Blue: End point
- White: Un-discovered point (i.e. not yet considered by algorithm)
- Black: Wall
- Red: Closed set (points that have already been considered by the algorithm)
- Green: Open set (points that are currently being considered by the algorithm)
- Violet: Final path from start to end