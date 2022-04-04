#import libraries
import pygame
import random

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
platform_image=pygame.image.load("assets/forma.png")

#game variables
GRAVITY = 1
MAX_PLATFORM=10



#define colors
WHITE=(255,255,255)


#player class
class Player():
    def __init__(self,x,y):
        self.image=pygame.transform.scale(batman_image,(60,60))
        self.width= 25
        self.height=40
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

        #check collision with platform
        for platform in platform_group:
            #platform in the y diretion
            if platform.rect.colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                #chech if  above  the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y>0:
                        self.rect.bottom=platform.rect.top
                        dy=0
                        self.vel_y =-20
                        


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


#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(platform_image, (width,20))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y


#player instance
batman = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 )

#create sprite groups
platform_group=pygame.sprite.Group()

#create temporary platforms
for p in range(MAX_PLATFORM):
    p_w= random.randint(40, 60)
    p_x= random.randint(0, SCREEN_WIDTH- p_w)
    p_y= p* random.randint(80, 120)
    platform= Platform(p_x,p_y,p_w)
    platform_group.add(platform)




#game loop
run = True
while run:

    #movement
    batman.move()
    clock.tick(FPS)

    #draw bg
    screen.blit(bg_image, (0, 0))

    #draw sprites
    platform_group.draw(screen)
    batman.draw()
    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
    
#update display window
    pygame.display.update()


pygame.quit()
