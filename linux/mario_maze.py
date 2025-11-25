import pygame
import random
import sys
import heapq

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 30
MAZE_COLS = 20
MAZE_ROWS = 15
FPS = 60

# Colors (Mario theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)  # Mario red
BLUE = (0, 120, 215)  # Sky blue
GREEN = (34, 177, 76)  # Goal green
YELLOW = (255, 215, 0)  # Coin yellow
BROWN = (139, 69, 19)  # Wall brown
LIGHT_BLUE = (135, 206, 250)  # Background

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
    """AI opponent using A* pathfinding algorithm"""
    def __init__(self, maze, start_pos, goal_pos):
        self.maze = maze
        self.pos = list(start_pos)
        self.goal = goal_pos
        self.path = []
        self.move_delay = 0
        self.move_speed = 8  # Moves every 8 frames (AI is slightly slower)
        
    def heuristic(self, pos):
        """Manhattan distance heuristic"""
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])
    
    def find_path(self):
        """A* pathfinding algorithm"""
        start = tuple(self.pos)
        goal = tuple(self.goal)
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start)}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            # Check neighbors
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if (0 <= neighbor[0] < len(self.maze[0]) and 
                    0 <= neighbor[1] < len(self.maze) and 
                    self.maze[neighbor[1]][neighbor[0]] == 0):
                    
                    tentative_g = g_score[current] + 1
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + self.heuristic(neighbor)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return []
    
    def update(self):
        """Update AI position"""
        self.move_delay += 1
        
        if self.move_delay >= self.move_speed:
            self.move_delay = 0
            
            if not self.path:
                self.path = self.find_path()
            
            if self.path:
                next_pos = self.path.pop(0)
                self.pos = list(next_pos)
    
    def draw(self, screen, offset_x, offset_y):
        """Draw AI player (Luigi - green)"""
        x = offset_x + self.pos[0] * CELL_SIZE
        y = offset_y + self.pos[1] * CELL_SIZE
        
        # Draw Luigi (green Mario)
        pygame.draw.circle(screen, GREEN, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
        # Hat
        pygame.draw.rect(screen, GREEN, (x + 5, y + 5, CELL_SIZE - 10, 8))
        # Eyes
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
    
    def draw(self, screen, offset_x, offset_y):
        """Draw player (Mario - red)"""
        x = offset_x + self.pos[0] * CELL_SIZE
        y = offset_y + self.pos[1] * CELL_SIZE
        
        # Draw Mario
        pygame.draw.circle(screen, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
        # Hat
        pygame.draw.rect(screen, RED, (x + 5, y + 5, CELL_SIZE - 10, 8))
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
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        """Reset game state"""
        # Generate maze
        generator = MazeGenerator(MAZE_COLS, MAZE_ROWS)
        self.maze = generator.generate()
        
        # Initialize players
        self.player = Player(self.maze, [0, 0])
        self.ai = AIPlayer(self.maze, [0, 0], [MAZE_COLS - 1, MAZE_ROWS - 1])
        self.goal = [MAZE_COLS - 1, MAZE_ROWS - 1]
        
        # Game state
        self.game_over = False
        self.winner = None
        self.running = True
        
    def draw_maze(self):
        """Draw the maze"""
        offset_x = (WINDOW_WIDTH - MAZE_COLS * CELL_SIZE) // 2
        offset_y = 80
        
        for row in range(MAZE_ROWS):
            for col in range(MAZE_COLS):
                x = offset_x + col * CELL_SIZE
                y = offset_y + row * CELL_SIZE
                
                if self.maze[row][col] == 1:
                    # Wall
                    pygame.draw.rect(self.screen, BROWN, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
                else:
                    # Path
                    pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw goal
        goal_x = offset_x + self.goal[0] * CELL_SIZE
        goal_y = offset_y + self.goal[1] * CELL_SIZE
        pygame.draw.rect(self.screen, GREEN, (goal_x, goal_y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLACK, (goal_x, goal_y, CELL_SIZE, CELL_SIZE), 2)
        
        # Draw "GOAL" text
        goal_text = self.small_font.render("GOAL", True, WHITE)
        self.screen.blit(goal_text, (goal_x + 2, goal_y + 8))
        
        return offset_x, offset_y
    
    def check_winner(self):
        """Check if someone reached the goal"""
        if self.player.pos == self.goal:
            self.game_over = True
            self.winner = "Mario"
        elif self.ai.pos == self.goal:
            self.game_over = True
            self.winner = "Luigi"
    
    def draw_ui(self):
        """Draw user interface"""
        # Title
        title = self.font.render("Mario Maze Race!", True, RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
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
            
            restart_text = self.small_font.render("Press R to Restart or Q to Quit", True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 575))
            self.screen.blit(restart_text, restart_rect)
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
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
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(LIGHT_BLUE)
        offset_x, offset_y = self.draw_maze()
        self.player.draw(self.screen, offset_x, offset_y)
        self.ai.draw(self.screen, offset_x, offset_y)
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
