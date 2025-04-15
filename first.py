import pygame
import random
import time

class Game:
    def __init__(self):
        #Init pygame
        pygame.init()
        pygame.display.set_caption("First Pygame [SnAkE] :D")
        self.font = pygame.font.SysFont('times new roman', 35)
        
        self.score = 0
        self.window = pygame.display.set_mode((500, 500))

        #important colors
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.white = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)

        #snake speed
        self.speed = 8

        #snake head
        self.head = [100, 50]
        self.snake = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.next_direction = self.direction

        #~~~~~fruit~~~~~
        self.eaten = False
        #fruit start position
        self.fruit_pos = (random.randrange(1, (self.window.get_width() // 10)) * 10,
                          random.randrange(1, (self.window.get_height() // 10)) * 10)
        
    #~~~~~score~~~~~
    def show_score(self):
        score_surface = self.font.render('Score : ' + str(self.score), True, self.white)
        score_rect = score_surface.get_rect()
        self.window.blit(score_surface, score_rect)

     #~~~~~spawn fruit~~~~~
    def spawn_fruit(self):
        self.fruit_pos = (random.randrange(1, (self.window.get_width() // 10)) * 10,
                              random.randrange(1, (self.window.get_height() // 10)) * 10)
        pygame.draw.rect(self.window, self.red, pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], 10, 10)) 

    #~~~~~keyboard input~~~~~
    def keyboard_input(self, key):
        if key == pygame.K_UP:
            self.next_direction = 'UP'
        if key == pygame.K_DOWN:
            self.next_direction = 'DOWN'
        if key == pygame.K_LEFT:
            self.next_direction = 'LEFT'
        if key == pygame.K_RIGHT:
            self.next_direction = 'RIGHT'

        #make sure snake can't go back on itself
        if self.next_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.next_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.next_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.next_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        
    #~~~~~Snake movement~~~~~
    def move_snake(self):
        #draw first fruit
        pygame.draw.rect(self.window, self.red, pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], 10, 10))
        #increase snake by 10
        self.snake.insert(0, list(self.head))
        #check if snake has eaten fruit
        if self.head[0] == self.fruit_pos[0] and self.head[1] == self.fruit_pos[1]:
            self.score += 10
            self.eaten = True
        else:
            self.snake.pop()
        #draw snake
        for pos in self.snake:
            pygame.draw.rect(self.window, self.green, pygame.Rect(pos[0], pos[1], 10, 10))
        #move snake in direction
        if self.direction == 'UP':
            self.head[1] -= 10
        if self.direction == 'DOWN':
            self.head[1] += 10
        if self.direction == 'LEFT':
            self.head[0] -= 10
        if self.direction == 'RIGHT':
            self.head[0] += 10
        #check if snake has hit wall or itself
        if self.head[0] < 0 or self.head[0] > (self.window.get_width() - 10) or self.head[1] < 0 or self.head[1] > (self.window.get_height() - 10):
            self.game_over()
        for block in self.snake[1:]:
            if self.head[0] == block[0] and self.head[1] == block[1]:
                self.game_over()

    #~~~~~game over~~~~~
    def game_over(self):
        #show score
        game_over_surface = self.font.render('Game Over! Score : ' + str(self.score), True, self.white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window.get_width() / 2, self.window.get_height() / 4)
        self.window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        quit()
    
    #+~~~~~Game loop~~~~~
    def start(self):
        #fps control
        fps = pygame.time.Clock()

        while True:
            #fill window with black
            self.window.fill((0, 0, 0, 0))
            self.window.set_alpha(128)
            #dispay score
            self.show_score()
            #check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    self.keyboard_input(event.key)
            #move snake
            self.move_snake()
            #check if fruit has been eaten
            if self.eaten:
                self.spawn_fruit()
                #increase speed as it eats food
                self.speed += 0.5
                self.eaten = False
            #update display
            pygame.display.update()
            #set fps
            fps.tick(self.speed)     

if __name__ == "__main__":
    game = Game()
    game.start()   

