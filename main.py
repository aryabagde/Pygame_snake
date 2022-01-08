#This time we will be trying in OOPs way
import pygame
import time
import random

Size = 24                                                       #size of image is 24 pixels

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,33)*Size
        self.y = random.randint(1,25)*Size

    def move(self):
        self.x = random.randint(1,33)*Size
        self.y = random.randint(1,25)*Size

class Snake:
    def __init__(self, surface, length):
        self.parent_screen = surface
        self.block = pygame.image.load("resources/square.png").convert()   #Adding snake image to the window
        self.length = length
        self.x = [Size]*length                                                     # with co-ordinates 
        self.y = [Size]*length
        self.direction = "down"

    def move_left(self):
        if(self.direction == "up" or self.direction == "down"):
            self.direction = "left"

    def move_right(self):
        if(self.direction == "up" or self.direction == "down"):
            self.direction = "right"

    def move_up(self):                                                     #x will be same
        if(self.direction == "left" or self.direction == "right"):
            self.direction = "up"

    def move_down(self):
        if(self.direction == "left" or self.direction == "right"):
            self.direction = "down"

    def draw(self):
        self.parent_screen.fill((255, 255, 255))                          # in order to show changes in the snake box
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))             # we will first color the previous block with the background 
        pygame.display.flip()                                             #color and then draw box to new position
                                                                          # we can use .flip() or .update() and .blit() means to draw

    def walk(self):   
        
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
                                                            # so that the snake keep moving on it's own
        if self.direction == "left":
            self.x[0] -= Size
        if self.direction == "down":
            self.y[0] += Size
        if self.direction == "up":
            self.y[0] -= Size
        if self.direction == "right":
            self.x[0] += Size
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()                                                     # Inititaiting pygame
        self.surface = pygame.display.set_mode((792, 600))                # creating window of size 500 x 500
        print(self.surface)                                               # we need self.surface for .blit() and .fill() which are in snake class
        self.snake = Snake(self.surface, 2)                                  
        self.snake.draw()                                                 # since draw function is in snake class
        self.apple = Apple(self.surface)
        self.apple.draw()


    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(255,0,0))
        self.surface.blit(score,(650,60))

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)


    def show_game_over(self):
        self.surface.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + Size:
            if y1 >= y2 and y1 < y2 + Size:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"
        

    def run(self):                                                        # so that the window appears till the users quit
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:                          # when the user presses any button
                    if event.key == pygame.K_ESCAPE:                      # escape button
                        running = False                                   # break the loop and end the game
                    if event.key == pygame.K_RETURN:
                        pause = False
                    
                    if not pause:

                        if event.key == pygame.K_LEFT:                        #left button
                            self.snake.move_left()

                        if event.key == pygame.K_RIGHT:
                            self.snake.move_right()

                        if event.key == pygame.K_UP:
                            self.snake.move_up()

                        if event.key == pygame.K_DOWN:
                            self.snake.move_down()

                elif event.type == pygame.QUIT:                            # cross buttton
                    running = False

            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)

if __name__ == '__main__':
    game = Game()                                                          # game is the object of class Game()
    game.run()