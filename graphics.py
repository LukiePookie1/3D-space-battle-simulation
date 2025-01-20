def print_ascii_map(shipA, shipB, grid_size=25):
    """
    Prints a 2D (x-y) ASCII map of size 'grid_size'.
    The top-left corner is (0, grid_size-1).
    """
    xA, yA = int(round(shipA.position[0])), int(round(shipA.position[1]))
    xB, yB = int(round(shipB.position[0])), int(round(shipB.position[1]))

    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

    # Place A if within bounds
    if 0 <= xA < grid_size and 0 <= yA < grid_size:
        grid[yA][xA] = "A"

    # Place B if within bounds
    if 0 <= xB < grid_size and 0 <= yB < grid_size:
        grid[yB][xB] = "B"

    # Print from top row to bottom row
    for row in reversed(grid):
        print("".join(row))
    print()  
