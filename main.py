#import libraries
import pygame

#initialise pygame
pygame.init()

#game window
SCREEN_WIDTH= 400
SCREEN_HEIGHT= 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Gotham')

#load images
bg_image = pygame.image.load("assets/bg.jpg").convert_alpha()
batman_image = pygame.image.load("assets/batman.png").convert_alpha()


#define colors
WHITE=(255,255,255)


#player class
class Player():
    def __init__(self,x,y):
        self.image=pygame.transform.scale(batman_image,(90,90))
        self.width= 45
        self.height=75 
        self.rect= pygame.Rect(0,0, self.width, self.height)
        self.rect.center =(x,y)
    
    def draw(self):
        screen.blit(self.image,(self.rect.x-20,self.rect.y-5))
        pygame.draw.rect(screen,WHITE,self.rect,2)

batman = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 )

#game loop
run = True
while run:

    #draw bg
    screen.blit(bg_image, (0, 0))

    #draw sprites
    batman.draw()
    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
    
#update display window
    pygame.display.update()


pygame.quit()
