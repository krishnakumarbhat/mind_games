import pygame
import random
import sys
import heapq
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
FONT_SIZE = 36
SMALL_FONT_SIZE = 24

# Colors (Mario theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)  # Mario red
BLUE = (0, 120, 215)  # Sky blue
GREEN = (34, 177, 76)  # Goal green
YELLOW = (255, 215, 0)  # Coin yellow
BROWN = (139, 69, 19)  # Wall brown
LIGHT_BLUE = (135, 206, 250)  # Background


LEVELS = [
    {
        "name": "Beginner's A*",
        "algorithm": "a_star",
        "cols": 16,
        "rows": 12,
        "ai_speed": 8,
    },
    {
        "name": "Dijkstra Challenge",
        "algorithm": "dijkstra",
        "cols": 20,
        "rows": 14,
        "ai_speed": 7,
    },
    {
        "name": "BFS Blitz",
        "algorithm": "bfs",
        "cols": 24,
        "rows": 16,
        "ai_speed": 6,
    },
    {
        "name": "DFS Depth Dive",
        "algorithm": "dfs",
        "cols": 28,
        "rows": 18,
        "ai_speed": 6,
    },
    {
        "name": "Greedy Sprint",
        "algorithm": "greedy",
        "cols": 32,
        "rows": 22,
        "ai_speed": 5,
    },
    {
        "name": "Random Explorer",
        "algorithm": "random_walk",
        "cols": 36,
        "rows": 26,
        "ai_speed": 5,
    },
]

class MazeGenerator:
    """Generate a maze using depth-first search algorithm"""
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]  # 1 = wall, 0 = path
        
    def generate(self):
        # Start from top-left
        start_x, start_y = 0, 0
        self.grid[start_y][start_x] = 0
        stack = [(start_x, start_y)]
        visited = {(start_x, start_y)}
        
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        
        while stack:
            current_x, current_y = stack[-1]
            neighbors = []
            
            for dx, dy in directions:
                nx, ny = current_x + dx * 2, current_y + dy * 2
                if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in visited:
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                # Carve path
                self.grid[current_y + dy][current_x + dx] = 0
                self.grid[ny][nx] = 0
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Ensure start and goal are clear
        self.grid[0][0] = 0
        self.grid[self.rows - 1][self.cols - 1] = 0
        
        return self.grid

class AIPlayer:
    """AI opponent supporting multiple pathfinding algorithms"""

    def __init__(self, maze, start_pos, goal_pos, algorithm="a_star", move_speed=8):
        self.maze = maze
        self.pos = list(start_pos)
        self.goal = tuple(goal_pos)
        self.algorithm = algorithm
        self.path = []
        self.move_delay = 0
        self.move_speed = move_speed

    def heuristic(self, pos):
        """Manhattan distance heuristic"""
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

    def is_walkable(self, pos):
        x, y = pos
        return (
            0 <= x < len(self.maze[0])
            and 0 <= y < len(self.maze)
            and self.maze[y][x] == 0
        )

    def neighbors(self, pos):
        x, y = pos
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            neighbor = (x + dx, y + dy)
            if self.is_walkable(neighbor):
                yield neighbor

    def build_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path[1:]

    def path_a_star(self, start):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == self.goal:
                return self.build_path(came_from, current)

            for neighbor in self.neighbors(current):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def path_dijkstra(self, start):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current = heapq.heappop(frontier)
            if current == self.goal:
                return self.build_path(came_from, current)

            if current_cost > cost_so_far.get(current, float("inf")):
                continue

            for neighbor in self.neighbors(current):
                new_cost = current_cost + 1
                if new_cost < cost_so_far.get(neighbor, float("inf")):
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(frontier, (new_cost, neighbor))

        return []

    def path_bfs(self, start):
        queue = deque([start])
        came_from = {start: None}
        visited = {start}

        while queue:
            current = queue.popleft()
            if current == self.goal:
                return self.build_path(came_from, current)

            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return []

    def path_dfs(self, start):
        stack = [start]
        came_from = {start: None}
        visited = set()

        while stack:
            current = stack.pop()
            if current == self.goal:
                return self.build_path(came_from, current)

            if current in visited:
                continue

            visited.add(current)

            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                    stack.append(neighbor)

        return []

    def path_greedy(self, start):
        current = start
        came_from = {start: None}
        visited = {start}

        for _ in range(len(self.maze) * len(self.maze[0])):
            if current == self.goal:
                return self.build_path(came_from, current)

            neighbors = list(self.neighbors(current))
            if not neighbors:
                break

            neighbors.sort(key=self.heuristic)
            next_step = None
            for neighbor in neighbors:
                if neighbor not in visited:
                    next_step = neighbor
                    break
            if next_step is None:
                next_step = neighbors[0]

            visited.add(next_step)
            came_from[next_step] = current
            current = next_step

        return []

    def path_random_walk(self, start):
        current = start
        came_from = {start: None}
        visited = {start}

        for _ in range(len(self.maze) * len(self.maze[0])):
            if current == self.goal:
                return self.build_path(came_from, current)

            neighbors = list(self.neighbors(current))
            if not neighbors:
                break

            unvisited = [n for n in neighbors if n not in visited]
            next_step = random.choice(unvisited or neighbors)
            came_from[next_step] = current
            current = next_step
            visited.add(next_step)

        return []

    def compute_path(self):
        start = tuple(self.pos)
        if self.algorithm == "a_star":
            return self.path_a_star(start)
        if self.algorithm == "dijkstra":
            return self.path_dijkstra(start)
        if self.algorithm == "bfs":
            return self.path_bfs(start)
        if self.algorithm == "dfs":
            return self.path_dfs(start)
        if self.algorithm == "greedy":
            return self.path_greedy(start)
        if self.algorithm == "random_walk":
            return self.path_random_walk(start)
        return self.path_a_star(start)

    def update(self):
        """Update AI position"""
        self.move_delay += 1

        if self.move_delay >= self.move_speed:
            self.move_delay = 0

            if not self.path:
                self.path = self.compute_path()

            if self.path:
                next_pos = self.path.pop(0)
                self.pos = list(next_pos)

    def draw(self, screen, offset_x, offset_y, cell_size):
        """Draw AI player (Luigi - green)"""
        x = offset_x + self.pos[0] * cell_size
        y = offset_y + self.pos[1] * cell_size

        pygame.draw.circle(screen, GREEN, (x + cell_size // 2, y + cell_size // 2), cell_size // 3)
        pygame.draw.rect(screen, GREEN, (x + 5, y + 5, cell_size - 10, 8))
        pygame.draw.circle(screen, WHITE, (x + 12, y + 15, 3))
        pygame.draw.circle(screen, WHITE, (x + 18, y + 15, 3))
        pygame.draw.circle(screen, BLACK, (x + 12, y + 15, 2))
        pygame.draw.circle(screen, BLACK, (x + 18, y + 15, 2))

class Player:
    """Human player (Mario)"""
    def __init__(self, maze, start_pos):
        self.maze = maze
        self.pos = list(start_pos)
        
    def move(self, dx, dy):
        """Move player if valid"""
        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy
        
        if (0 <= new_x < len(self.maze[0]) and 
            0 <= new_y < len(self.maze) and 
            self.maze[new_y][new_x] == 0):
            self.pos[0] = new_x
            self.pos[1] = new_y
            return True
        return False
    
    def draw(self, screen, offset_x, offset_y, cell_size):
        """Draw player (Mario - red)"""
        x = offset_x + self.pos[0] * cell_size
        y = offset_y + self.pos[1] * cell_size
        
        # Draw Mario
        pygame.draw.circle(screen, RED, (x + cell_size // 2, y + cell_size // 2), cell_size // 3)
        # Hat
        pygame.draw.rect(screen, RED, (x + 5, y + 5, cell_size - 10, 8))
        # Eyes
        pygame.draw.circle(screen, WHITE, (x + 12, y + 15, 3))
        pygame.draw.circle(screen, WHITE, (x + 18, y + 15, 3))
        pygame.draw.circle(screen, BLACK, (x + 12, y + 15, 2))
        pygame.draw.circle(screen, BLACK, (x + 18, y + 15, 2))
        # Mustache
        pygame.draw.line(screen, BLACK, (x + 10, y + 20), (x + 20, y + 20), 2)

class MazeGame:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Mario Maze Race - Beat Luigi!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

        self.level_index = 0
        self.level_transition_time = None
        self.running = True
        self.reset_game()
        
    def compute_cell_size(self, cols, rows):
        max_cell_width = max(12, (WINDOW_WIDTH - 120) // cols)
        max_cell_height = max(12, (WINDOW_HEIGHT - 200) // rows)
        return min(40, max_cell_width, max_cell_height)
        
    def reset_game(self):
        """Reset game state"""
        level = LEVELS[self.level_index]
        self.level_name = level["name"]
        self.level_algorithm = level["algorithm"]
        self.cols = level["cols"]
        self.rows = level["rows"]
        self.cell_size = self.compute_cell_size(self.cols, self.rows)

        generator = MazeGenerator(self.cols, self.rows)
        self.maze = generator.generate()
        
        # Initialize players
        self.player = Player(self.maze, [0, 0])
        self.goal = [self.cols - 1, self.rows - 1]
        self.ai = AIPlayer(
            self.maze,
            [0, 0],
            self.goal,
            algorithm=self.level_algorithm,
            move_speed=level["ai_speed"],
        )
        
        # Game state
        self.game_over = False
        self.winner = None
        self.level_transition_time = None

    def draw_maze(self):
        """Draw the maze"""
        offset_x = (WINDOW_WIDTH - self.cols * self.cell_size) // 2
        offset_y = 80
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * self.cell_size
                y = offset_y + row * self.cell_size
                
                if self.maze[row][col] == 1:
                    # Wall
                    pygame.draw.rect(self.screen, BROWN, (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(self.screen, BLACK, (x, y, self.cell_size, self.cell_size), 1)
                else:
                    # Path
                    pygame.draw.rect(self.screen, WHITE, (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(
                        self.screen,
                        (200, 200, 200),
                        (x, y, self.cell_size, self.cell_size),
                        1,
                    )
        
        # Draw goal
        goal_x = offset_x + self.goal[0] * self.cell_size
        goal_y = offset_y + self.goal[1] * self.cell_size
        pygame.draw.rect(self.screen, GREEN, (goal_x, goal_y, self.cell_size, self.cell_size))
        pygame.draw.rect(self.screen, BLACK, (goal_x, goal_y, self.cell_size, self.cell_size), 2)
        
        # Draw "GOAL" text
        goal_text = self.small_font.render("GOAL", True, WHITE)
        self.screen.blit(goal_text, (goal_x + 2, goal_y + 8))
        
        return offset_x, offset_y
    
    def check_winner(self):
        """Check if someone reached the goal"""
        if self.player.pos == self.goal:
            self.game_over = True
            self.winner = "Mario"
            self.level_transition_time = pygame.time.get_ticks() + 2000
        elif self.ai.pos == self.goal:
            self.game_over = True
            self.winner = "Luigi"
            self.level_transition_time = pygame.time.get_ticks() + 2000

    def draw_ui(self):
        """Draw user interface"""
        # Title
        title = self.font.render("Mario Maze Race!", True, RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        level_text = self.small_font.render(
            f"Level {self.level_index + 1}: {self.level_name} ({self.level_algorithm.upper()})",
            True,
            BLACK,
        )
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(level_text, level_rect)

        # Instructions
        if not self.game_over:
            instructions = self.small_font.render("Use Arrow Keys - Beat Luigi to the Goal!", True, BLACK)
            inst_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, 560))
            self.screen.blit(instructions, inst_rect)
        
        # Game Over
        if self.game_over:
            if self.winner == "Mario":
                result_text = self.font.render("YOU WIN! 🎉", True, GREEN)
            else:
                result_text = self.font.render("LUIGI WINS! 😅", True, BLUE)
            
            result_rect = result_text.get_rect(center=(WINDOW_WIDTH // 2, 540))
            self.screen.blit(result_text, result_rect)
            
            restart_text = self.small_font.render("Press R to Replay Level or Q to Quit", True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 575))
            self.screen.blit(restart_text, restart_rect)

            if self.level_transition_time is not None:
                transition_text = self.small_font.render("Advancing to next level...", True, BLUE)
                transition_rect = transition_text.get_rect(center=(WINDOW_WIDTH // 2, 520))
                self.screen.blit(transition_text, transition_rect)

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return
                    elif event.key == pygame.K_q:
                        self.running = False
                else:
                    if event.key == pygame.K_UP:
                        self.player.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.player.move(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.player.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(1, 0)
    
    def update(self):
        """Update game state"""
        if not self.game_over:
            self.ai.update()
            self.check_winner()
        else:
            if self.level_transition_time and pygame.time.get_ticks() >= self.level_transition_time:
                self.level_index = (self.level_index + 1) % len(LEVELS)
                self.reset_game()

    def draw(self):
        """Draw everything"""
        self.screen.fill(LIGHT_BLUE)
        offset_x, offset_y = self.draw_maze()
        self.player.draw(self.screen, offset_x, offset_y, self.cell_size)
        self.ai.draw(self.screen, offset_x, offset_y, self.cell_size)
        self.draw_ui()
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MazeGame()
    game.run()
