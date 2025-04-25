import pygame
import random

# Configs
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
FPS = 60

# Colors
BG = (150, 150, 150)
LINE = (0, 0, 0)
VISITED = (100, 200, 255)
CURRENT = (100, 255, 100)
PATH = (255, 255, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze!")
clock = pygame.time.Clock()

class Cell:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.visited = False
        self.walls = [True] * 4  # top, right, bottom, left
        self.in_path = False

    def draw(self, surf, current = False):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.in_path:
            pygame.draw.rect(surf, PATH, (x, y, CELL_SIZE, CELL_SIZE))
        elif self.visited:
            pygame.draw.rect(surf, VISITED, (x, y, CELL_SIZE, CELL_SIZE))

        if current:
            pygame.draw.rect(surf, CURRENT, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls[0]: pygame.draw.line(surf, LINE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]: pygame.draw.line(surf, LINE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]: pygame.draw.line(surf, LINE, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]: pygame.draw.line(surf, LINE, (x, y + CELL_SIZE), (x, y), 2)

    def check_neighbors(self, grid):
        neighbors = []

        def valid(r, c):
            return 0 <= r < ROWS and 0 <= c < COLS and not grid[r][c].visited

        directions = [(self.row - 1, self.col), (self.row, self.col + 1),
                      (self.row + 1, self.col), (self.row, self.col - 1)]

        for i, (r, c) in enumerate(directions):
            if valid(r, c):
                neighbors.append((grid[r][c], i))

        return random.choice(neighbors) if neighbors else None

def remove_walls(a, b, direction):
    if direction == 0:
        a.walls[0] = False
        b.walls[2] = False
    elif direction == 1:
        a.walls[1] = False
        b.walls[3] = False
    elif direction == 2:
        a.walls[2] = False
        b.walls[0] = False
    elif direction == 3:
        a.walls[3] = False
        b.walls[1] = False

def make_grid():
    return [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]

def draw_grid(win, grid, current):
    win.fill(BG)
    for row in grid:
        for cell in row:
            cell.draw(win, current == cell)
    pygame.display.flip()

def solve_maze(grid):
    start = grid[0][0]
    end = grid[ROWS - 1][COLS - 1]
    stack = [(start, [])]
    visited = set()

    while stack:
        pygame.time.delay(10)
        draw_grid(win, grid, None)

        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == end:
            for cell in path:
                cell.in_path = True
                draw_grid(win, grid, None)
                pygame.time.delay(20)
            return

        r, c = current.row, current.col
        neighbors = []
        if not current.walls[0]: neighbors.append(grid[r - 1][c])
        if not current.walls[1]: neighbors.append(grid[r][c + 1])
        if not current.walls[2]: neighbors.append(grid[r + 1][c])
        if not current.walls[3]: neighbors.append(grid[r][c - 1])

        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path))

def main():
    grid = make_grid()
    stack = []
    current = grid[0][0]
    current.visited = True
    generating = True
    solved = False

    running = True
    while running:
        clock.tick(FPS)
        draw_grid(win, grid, current if generating else None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not generating and not solved:
                    solve_maze(grid)
                    solved = True

        if generating:
            next_cell_data = current.check_neighbors(grid)
            if next_cell_data:
                next_cell, dir = next_cell_data
                stack.append(current)
                remove_walls(current, next_cell, dir)
                current = next_cell
                current.visited = True
            elif stack:
                current = stack.pop()
            else:
                generating = False

    pygame.quit()

if __name__ == "__main__":
    main()