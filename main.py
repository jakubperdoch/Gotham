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

#framerate
clock=pygame.time.Clock()
FPS= 60

#load images
bg_image = pygame.image.load("assets/bg.jpg").convert_alpha()
batman_image = pygame.image.load("assets/batman.png").convert_alpha()

#game variables
GRAVITY = 1


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
        self.vel_y=0
        self.flip=False
    
    def move(self):

        #reset variables
        dx=0
        dy=0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx= -10
            self.flip=True
        if key[pygame.K_d]:
            dx= +10
            self.flip=False

        #gravity
        self.vel_y +=GRAVITY
        dy += self.vel_y

        #ensure player doesnt go off the edge of the screen
        if self.rect.left +dx <0:
            dx=- self.rect.left

        if self.rect.right +dx > SCREEN_WIDTH:
            dx= SCREEN_WIDTH - self.rect.right

        #check collision with ground
        if self.rect.bottom +dy > SCREEN_HEIGHT:
            dy=0
            self.vel_y =-20

        #update rect position
        self.rect.x +=dx
        self.rect.y +=dy
       

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip, False),(self.rect.x-20,self.rect.y-5))
        pygame.draw.rect(screen,WHITE,self.rect,2)

batman = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 )

#game loop
run = True
while run:

    #movement
    batman.move()
    clock.tick(FPS)

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
