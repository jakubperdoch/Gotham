#import libraries
import pygame #import pygame
import random #import random
import os

#initialise pygame
pygame.init()

#game window
SCREEN_WIDTH= 400 #šírka
SCREEN_HEIGHT= 600 #výška

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #vykreslenie okna
pygame.display.set_caption('Gotham') # nazov hry 

#framerate
clock=pygame.time.Clock()
FPS= 60

#load images
bg_image = pygame.image.load("assets/bg.jpg").convert_alpha()
batman_image = pygame.image.load("assets/batman.png").convert_alpha()
platform_image=pygame.image.load("assets/forma.png")

#game variables
GRAVITY = 1
SCROLL_THRESH= 200
MAX_PLATFORM=12
scroll=0
game_over = False
score=0
fade_counter=0


if os.path.exists('score.txt'):
    with open('score.txt','r') as file:
        high_score= int(file.read())
else:
    high_score=0


#define colors
WHITE=(255,255,255)
BLACK=(0,0,0)
PANEL=(0,0,0)

#fonts
font_small= pygame.font.SysFont("Lucida Sans", 20)
font_big= pygame.font.SysFont("Lucida Sans", 27)
font_vbig= pygame.font.SysFont("Lucida Sans", 40)



#function for outputting text onto screen
def draw_text(text,font,text_color,x,y):
    img= font.render(text,True,text_color)
    screen.blit(img, (x,y))


#function for drawing info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0,0,SCREEN_WIDTH,30))
    pygame.draw.line(screen,WHITE,(0,30),(SCREEN_WIDTH,30),3)
    draw_text("SCORE: " +str(score),font_small,WHITE,0,0)
    





#player class
class Player():
    def __init__(self,x,y):
        self.image=pygame.transform.scale(batman_image,(60,60)) #velkost postavicky
        self.width= 25 #nastavene kolizie okolo postavy
        self.height=40 #nastavene kolizie okolo postavy
        self.rect= pygame.Rect(0,0, self.width, self.height)
        self.rect.center =(x,y)
        self.vel_y=0
        self.flip=False #zakladne otocenie postavy do prava
    
    def move(self):

        #reset variables
        dx=0
        dy=0
        scroll=0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx= -10
            self.flip=True #otocenie postavy do lava
        if key[pygame.K_d]:
            dx= +10
            self.flip=False #otocenie postavy do prava

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
                        


        
        

        #check if the player has bounced to the top of the screen
        if self.rect.top<=SCROLL_THRESH:
            #if player is jumping
            if self.vel_y<0:
                scroll= -dy
            

        #update rect position
        self.rect.x +=dx
        self.rect.y +=dy + scroll 

        return scroll
       

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip, False),(self.rect.x-20,self.rect.y-5)) #otacanie postavy
        pygame.draw.rect(screen,WHITE,self.rect,2)


#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(platform_image, (width,20))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    
    def update(self,scroll):

        #update platform vert postition
        self.rect.y +=scroll

        #check if platform has gone off the screen
        if self.rect.top >SCREEN_HEIGHT: #aby nebola platforma mimo mapy
            self.kill()




#player instance
batman = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 ) #zaciatocna pozicia hraca

#create sprite groups
platform_group=pygame.sprite.Group()

#create  starting platform
platform=Platform(SCREEN_WIDTH //2-50, SCREEN_HEIGHT-50, 100) #rozmery zaciatocnej platformy
platform_group.add(platform)




#game loop
run = True
while run:

    
    clock.tick(FPS)


    #GAME OVER
    if game_over == False: 
    
        #movement
        scroll=batman.move()

        #draw bg
        screen.blit(bg_image, (0, 0))


        #generate platforms
        if len(platform_group)<MAX_PLATFORM:
            p_w = random.randint(40, 60) #rozmedzie sirky platform
            p_x = random.randint(0, SCREEN_WIDTH-  p_w) #pozicia platform x os
            p_y = platform.rect.y -random.randint(80, 120) #pozicia platform y os
            platform=Platform(p_x, p_y, p_w) 
            platform_group.add(platform)

        print(len(platform_group)) 

        #update score
        if scroll > 0:
            score += scroll #skore sa updtatuje podla dosiahnutej vysky


        #draw line at previous high score
        pygame.draw.line(screen, WHITE, (0,score-high_score + SCROLL_THRESH),(SCREEN_WIDTH,score-high_score + SCROLL_THRESH),3) #čiara zaznačujúca high score
        draw_text('HIGH SCORE',font_small,WHITE,SCREEN_WIDTH-130,score-high_score + SCROLL_THRESH) #napis "high score" pod ciarou

        #update platforms
        platform_group.update(scroll)

        #draw sprites
        platform_group.draw(screen) # vykreslenie platform
        batman.draw() #vykreslenie postavy

        #draw panel
        draw_panel()

        

    #check game over
        if batman.rect.top>SCREEN_HEIGHT:
            game_over=True

    else:
        if fade_counter<SCREEN_WIDTH:
            fade_counter +=5 
            for y in range(0,6,2):

                pygame.draw.rect(screen, BLACK, (0,y*100,fade_counter,100)) #uzatvorenie obrazovky
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH -fade_counter,(y+1)*100,SCREEN_WIDTH,100)) #uzatvorenie obrazovky z druhej strany

                #update high score
            if score> high_score:
                high_score= score
                with open('score.txt','w') as file:
                    file.write(str(high_score))

        else:
            draw_text("GAME OVER !",font_vbig,WHITE,85,125)
            draw_text("SCORE: " +str(score),font_big, WHITE, 20, 250)
            draw_text("PRESS SPACE TO PLAY OVER",font_big,WHITE,20 ,400 )
            draw_text("HIGH SCORE: " +str(high_score),font_big,WHITE,20,300)
            
            

            
            
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                #reset variables
                game_over=False
                score=0
                scroll=0
                fade_counter=0
                #reposition batman
                batman.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 )
                #reset platforms
                platform_group.empty()
                platform=Platform(SCREEN_WIDTH //2-50, SCREEN_HEIGHT-50, 100)
                platform_group.add(platform)


    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score> high_score:
                high_score= score
                with open('score.txt','w') as file:
                    file.write(str(high_score))
            run= False
    
#update display window
    pygame.display.update()


pygame.quit()
