import pygame
import random
import sys

white = ("#FFFFFF")
red = ("#FF0000")
black = ("#000000")
gray = ("#333333")
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700 
GRID_SIZE = 50
BLOCK_SIZE = 40
GAME_SPEED = 10
SNAKE_SIZE = 4

class Food:
    def __init__(self, game):
         self.game = game
         self.x = GRID_SIZE*random.randint(1, 13) + 6
         self.y = GRID_SIZE*random.randint(1, 13) + 6
         self.rect = (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self):
         pygame.draw.rect(self.game.window, red, self.rect)

class Snake:
        def __init__(self, game, food):
            self.food = food
            self.game = game
            self.x = 3*GRID_SIZE + 6
            self.y = 3*GRID_SIZE + 6
            self.rect = (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.direction = (GRID_SIZE, 0)
            self.size = SNAKE_SIZE
            self.segments = []
            self.score = 0

        def move(self):
            self.x += self.direction[0]
            self.y += self.direction[1]
            self.rect = (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.segments.append((self.x , self.y))
            self.segments = self.segments[-self.size:]

        def change_direction(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0 , GRID_SIZE) :
                    self.direction = (0 , -GRID_SIZE)
                if event.key == pygame.K_DOWN and self.direction != (0 , -GRID_SIZE):
                    self.direction = (0 , GRID_SIZE)
                if event.key == pygame.K_LEFT and self.direction != (GRID_SIZE , 0):
                    self.direction = (-GRID_SIZE , 0)
                if event.key == pygame.K_RIGHT and self.direction != (-GRID_SIZE , 0):
                    self.direction = (GRID_SIZE , 0)

        def check_borders(self):
            if self.x <= 0 or self.x >= WINDOW_WIDTH or self.y <= 0 or self.y >= WINDOW_HEIGHT:
                self.game.new_game()

        def eat(self):
            if pygame.Rect(self.rect).colliderect(pygame.Rect(self.food.rect)):
                self.food.x = GRID_SIZE*random.randint(1, 13) + 6
                self.food.y = GRID_SIZE*random.randint(1, 13) + 6
                self.food.rect = (self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE)
                self.size += 1
                self.score += 1

        def check_self_eating(self):
            if len(self.segments) > 1:
                head = self.segments[-1]
                for segment in self.segments[:-1]:
                    if head[0] == segment[0] and head[1] == segment[1]:
                        self.game.new_game()

        def update_screen(self):
            self.move()
            self.eat()
            self.check_self_eating()
            self.check_borders()

        def draw(self):
            for segment in self.segments:
                pygame.draw.rect(self.game.window, white, (segment[0], segment[1] , BLOCK_SIZE , BLOCK_SIZE)) 

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("SNAKE GAME")
        self.clock = pygame.time.Clock()
        self.new_game()
    
    def score(self):
        font = pygame.font.Font(None, 55)
        score_keeper = font.render(f'Score: {self.snake.score}', True, white)
        self.window.blit(score_keeper, (10,10))


    def grid(self):
        for x in range(0,WINDOW_WIDTH,GRID_SIZE):
            pygame.draw.line(self.window, gray, (x,0), (x, WINDOW_WIDTH),2)
        for y in range(0,WINDOW_HEIGHT,GRID_SIZE):
            pygame.draw.line(self.window, gray, (0,y), (WINDOW_HEIGHT, y),2)

    def draw(self):
        self.window.fill(black)
        self.grid()
        self.food.draw()
        self.snake.draw()
        self.score()

    def new_game(self):
        self.food  = Food(self)
        self.snake = Snake(self, self.food)

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.snake.change_direction(event)
            self.snake.check_borders()
            self.snake.eat()
            self.snake.check_self_eating()


    def update_screen(self):
        self.snake.update_screen()
        pygame.display.update()
        self.clock.tick(GAME_SPEED)

    def run(self):
        while True:
            self.draw()
            self.check_event()
            self.update_screen()

if __name__ == '__main__':
    game = Game()
    game.run()
