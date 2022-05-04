#import libraries
import pygame #import pygame
import random #import random
import os #import os
from pygame import mixer#import pre hudbu

#initialise pygame
mixer.init()
pygame.init()

#game window
SCREEN_WIDTH= 400 #šírka
SCREEN_HEIGHT= 600 #výška

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #vykreslenie okna
pygame.display.set_caption('Gotham') # nazov hry 

#framerate
clock=pygame.time.Clock() #premena do ktorej zadam fpska
FPS= 45 #frame per second

#load music and sounds
death_fx=pygame.mixer.Sound("assets/death.wav")#nacitanie soundu smrti
death_fx.set_volume(0.5)#jeho hlasitost

jump_fx=pygame.mixer.Sound("assets/jump.wav")#nacitanie soundu jumpu
jump_fx.set_volume(0.5)#jeho hlasitost

pygame.mixer.music.load("assets/gotham.wav")#nacitanie hudby
pygame.mixer.music.set_volume(0.3)#jeho hlasitost
pygame.mixer.music.play(-1,0.0)#ze sa ma opakovat do nekonecna a od zacati hry

#load images
bg_image = pygame.image.load("assets/bg.jpg").convert_alpha() #nacita obrazok pozadia
batman_image = pygame.image.load("assets/batman.png").convert_alpha() #nacita obrazok postavicky
platform_image=pygame.image.load("assets/forma.png")#nacita obrazok platformy
wing =pygame.image.load("assets/wing.png").convert_alpha()#nacita obrazok enemaka/stihacky


#game variables
GRAVITY = 1 #premena ktora pritahuje postavicku nadol
SCROLL_THRESH= 200 #premena priestor medzi postavvou a vrskom mapy
MAX_PLATFORM=7#maximalny pocet platfrom na jednej obrazovke
scroll=0 #premena kotra sa stara  o posuvanie na dalsiu obrazovku
game_over = False #aby sa mohla zacat hra
score=0# zacinajuce skore
fade_counter=0#uzatvorenie obrazovky



if os.path.exists('score.txt'): #ak score.txt existuje tak si zoberie z neho high score 
    with open('score.txt','r') as file:
        high_score= int(file.read())
else: #ak dokument neexistuje zacinajuce skore sa rovna nule
    high_score=0


#define colors
WHITE=(255,255,255) #biela
BLACK=(0,0,0)# ciena
PANEL=(0,0,0)#farba horneho panelu

#fonts
font_small= pygame.font.SysFont("Lucida Sans", 20)#male pismo
font_big= pygame.font.SysFont("Lucida Sans", 27)#velke pismo
font_vbig= pygame.font.SysFont("Lucida Sans", 40)#este vacsie pismo



#function for outputting text onto screen
def draw_text(text,font,text_color,x,y):#definicia na vykreslenie textu na game over obrazovku
    img= font.render(text,True,text_color)#
    screen.blit(img, (x,y))


#function for drawing info panel
def draw_panel(): #panel so score
    pygame.draw.rect(screen, PANEL, (0,0,SCREEN_WIDTH,30))#pozadie tabulky
    pygame.draw.line(screen,WHITE,(0,30),(SCREEN_WIDTH,30),3)#ciara oddelujuca hru a tabulku
    draw_text("SCORE: " +str(score),font_small,WHITE,0,0)#vypisuje score pocas hry
    

#player class
class Player(): #vlastnosti hraca a jeho parametre
    def __init__(self,x,y):
        self.image=pygame.transform.scale(batman_image,(60,60)) #velkost postavicky
        self.width= 25 #nastavene kolizie okolo postavy
        self.height=40 #nastavene kolizie okolo postavy
        self.rect= pygame.Rect(0,0, self.width, self.height)#vytvorenie stvorca pre kolizie -neskor ho dopasujeme do obrazka
        self.rect.center =(x,y)#poloha postavy 
        self.vel_y=0
        self.flip=False #zakladne otocenie postavy do prava
        
    
    def move(self):

        #reset variables -pred tym este ako pouzijeme tieto premenne tak ich vyresetujeme na 0
        dx=0
        dy=0
        scroll=0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:#po stlaceni klavesi A
            dx= -10#pohyb do lava
            self.flip=True #otocenie postavy do lava
        if key[pygame.K_d]:#po stlaceni klavesi D
            dx= +10#pohyb do prava
            self.flip=False #otocenie postavy do prava

        #gravity
        self.vel_y +=GRAVITY #pohyb hraca nadol-gravitacia 
        dy += self.vel_y

        #ensure player doesnt go off the edge of the screen
        if self.rect.left +dx <0: #aby hrac nevysiel mimo mapu ale aby sa mohol max dotknut okraja -lava str
            dx=- self.rect.left#kolko maximalne sa moze pohnut do lava

        if self.rect.right +dx > SCREEN_WIDTH:#aby hrac nevysiel mimo mapu ale aby sa mohol max dotknut okraja -prava str
            dx= SCREEN_WIDTH - self.rect.right#kolko maximalne sa moze pohnut do prava

        #check collision with platform
        for platform in platform_group:
            #collision in the y diretion
            if platform.rect.colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):#kontrola ci dojde ku "zrazke"
                #chech if  above  the platform
                if self.rect.bottom < platform.rect.centery:#ak sa postava nachadza nad platformou
                    if self.vel_y>0: # a ak pada
                        self.rect.bottom=platform.rect.top#aby sa spravne dotykali kolizie postavy a platformy
                        dy=0
                        self.vel_y =-20#velocity bude zmensena tym padom bude skakat
                        jump_fx.play()#zvuk skoku
                        

        #check if the player has bounced to the top of the screen
        if self.rect.top<=SCROLL_THRESH:#ak sa postava nachadza nad scroll threhs- ,zacne sa nacitavat nova a plocha pod nim zanikne
            #if player is jumping
            if self.vel_y<0:#jedine ak sa postava posuva nahor-nie nadol
                scroll= -dy
            

        #update rect position
        self.rect.x +=dx
        self.rect.y +=dy + scroll 

        #update mask
        self.mask =pygame.mask.from_surface(self.image)#aby sa postava spravne dotykala enemaka

        return scroll
       

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip, False),(self.rect.x-20,self.rect.y-5)) #otacanie postavy a este aby postava pasovala do stvorca s koliziou
       

#enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH,y,img,scale):#klasa enemy bude pozostavat zo sirky obrazovky,y-osi,obrazku, a z velkosti
        pygame.sprite.Sprite.__init__(self)
        
        #define variables
        self.direction= random.choice([-1,1]) #random vyber smeru pohybu enemaka
        
        if self.direction==1: #aby sa enemak otocil spravnym smerom
            self.flip=True#do prava
        else:
            self.flip=False#do lava


        #load images
        wing =pygame.image.load("assets/wing.png").convert_alpha()#obrazok enemaka
        wing= pygame.transform.flip(wing, self.flip, False)#enemak sa otoci v smere pohybu
        self.image=pygame.transform.scale(wing,(110,100))#rozmery enemaka
        self.rect= self.image.get_rect()#enemak vlozeny do stvorca-pre kolizie 

        if self.direction==1:#podmienka aby enemak nesiel mimo mapu
            self.rect.x= 0 
        else:
            self.rect.x= SCREEN_WIDTH#
        self.rect.y= y

    def update(self,scroll,SCREEN_WIDTH,):
        
        #move enemy
        self.rect.x += self.direction * 2 #smer a rychlost enemaka
        self.rect.y +=scroll#enemak ostava na y polohe a nehybe sa s nami

        #check if it gone off screen
        if self.rect.right<0 or self.rect.left >SCREEN_WIDTH:#ked sa enemak dostane na okraj mapy bude vymazany
            self.kill()


#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width,moving):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(platform_image, (width,20))#zmena velkosti obrazku platformi
        self.moving= moving#moznost pohybu
        self.move_counter=random.randint(0, 50)#dlzka-cas pohybu
        self.direction= random.choice([-1,1])#vyber smeru pohybu
        self.speed =random.randint(1, 2)#vyber z dvoch rychlosti
        self.rect=self.image.get_rect()#vytvorenie stvorca okolo platformy pre kolizie
        self.rect.x=x
        self.rect.y=y
    
    def update(self,scroll):
        #move platform side to side if it is a moving platform
        if self.moving==True: #
            self.move_counter +=1#
            self.rect.x +=self.direction * self.speed #platformy mozu byt rozne rychle

        #change platform if it has moved fully or hit a wall
        if self.move_counter >=100 or self.rect.left <0 or self.rect.right >SCREEN_WIDTH: #ak sa platformi budu pohybovat dostatocne dlho alebo narazia do steny tak zmenia smer
            self.direction *= -1 #zmena na opacny smer pohybu
            self.move_counter =0#
 
        #update platform vert postition
        self.rect.y +=scroll#

        #check if platform has gone off the screen
        if self.rect.top >SCREEN_HEIGHT: #aby nebola platforma mimo mapy,ked prejdeme na dalsiu obrazovku
            self.kill()


#player instance
batman = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 ) #zaciatocna pozicia hraca

#create sprite groups
platform_group=pygame.sprite.Group()#pre ulozenie skupiny platform
enemy_group=pygame.sprite.Group()#pre ulozenie skupiny enemakov

#create  starting platform
platform=Platform(SCREEN_WIDTH //2-50, SCREEN_HEIGHT-50, 100,False) #rozmery zaciatocnej platformy
platform_group.add(platform)#pridanie zaciatocnej platformy do skupiny 


#game loop
run = True#
while run:

    clock.tick(FPS)

    #GAME OVER
    if game_over == False:  #pokial je hrac nazive tak sa odohra main game loop
    
        #movement
        scroll=batman.move() #pohyb postavicky

        #draw bg
        screen.blit(bg_image, (0, 0))#vykreslenie pozadia

        #generate platforms
        if len(platform_group)<MAX_PLATFORM:
            p_w = random.randint(40, 60) #rozmedzie sirky platform
            p_x = random.randint(0, SCREEN_WIDTH-  p_w) #pozicia platform x os
            p_y = platform.rect.y -random.randint(80, 120) #pozicia platform y os
            p_type=random.randint(1,2)#vyber z dvoch typov platform
            
            if p_type==1 and score>50: #ak sa tieto dve podmienky splnia zacnu sa generovat aj hybajuce sa platformy
                p_moving=True
            else:
                p_moving=False

            platform=Platform(p_x, p_y, p_w,p_moving)#
            platform_group.add(platform)#

        #update platforms
        platform_group.update(scroll)

        #generate enemies
        if len(enemy_group) ==0 and score>300: #mnozstvo  enemakov
            enemy=Enemy(SCREEN_WIDTH, 100, wing, 1.5)#parametre enemaka
            enemy_group.add(enemy)

        #update enemies
        enemy_group.update(scroll,SCREEN_WIDTH)

        #update score
        if scroll > 0:
            score += scroll #skore sa updatuje podla dosiahnutej vysky hraca


        #draw line at previous high score
        pygame.draw.line(screen, WHITE, (0,score-high_score + SCROLL_THRESH),(SCREEN_WIDTH,score-high_score + SCROLL_THRESH),3) #čiara zaznačujúca high score
        draw_text('HIGH SCORE',font_small,WHITE,SCREEN_WIDTH-130,score-high_score + SCROLL_THRESH) #napis "high score" pod ciarou

        #update platforms
        platform_group.update(scroll)#vykresluje plosiny do nekonecna

        #draw sprites
        platform_group.draw(screen) # vykreslenie platform
        batman.draw() #vykreslenie postavy
        enemy_group.draw(screen)#vykreslenie enemakov


        #draw panel
        draw_panel() #vzkresli panel so score 

        
    #check game over
        if batman.rect.top>SCREEN_HEIGHT: #aby sme nepadali do nekonecna
            game_over=True 
            death_fx.play()#aby zahral zvuk smrti
    #check for collision with enemy
        if pygame.sprite.spritecollide(batman, enemy_group, False,pygame.sprite.collide_mask):#ak sa postava "dotkne" enemaka je game over
            game_over=True
            death_fx.play()#aby zahral zvuk smrti
    else:
        if fade_counter<SCREEN_WIDTH:
            fade_counter +=5 #uzatvorenie hry po smrti ciernymi obdlznikami
            for y in range(0,6,2):
                pygame.draw.rect(screen, BLACK, (0,y*100,fade_counter,100)) #uzatvorenie obrazovky
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH -fade_counter,(y+1)*100,SCREEN_WIDTH,100)) #uzatvorenie obrazovky z druhej strany

                #update high score
            if score> high_score: #prepise najvyssie dosiahnute skore
                high_score= score
                with open('score.txt','w') as file:
                    file.write(str(high_score))

        else: #vypise score,...
            draw_text("GAME OVER !",font_vbig,WHITE,85,125)
            draw_text("SCORE: " +str(score),font_big, WHITE, 20, 250)
            draw_text("PRESS SPACE TO PLAY OVER",font_big,WHITE,20 ,400 )
            draw_text("HIGHEST SCORE: " +str(high_score),font_big,WHITE,20,300)
            draw_text("PRESS SHIFT FOR EXIT",font_big,WHITE,20,500)
            
            key=pygame.key.get_pressed()
            
            if key[pygame.K_SPACE]: #zresetovanie parametrov a pozicie postavy ak stlacime enter
                #reset variables
                game_over=False
                score=0
                scroll=0
                fade_counter=0
                #reposition batman
                batman.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 )
                #reset enemy
                enemy_group.empty()
                #reset platforms
                platform_group.empty()
                platform=Platform(SCREEN_WIDTH //2-50, SCREEN_HEIGHT-50, 100,False)
                platform_group.add(platform)
            if key[pygame.K_LSHIFT ]: #ukoncenie hry po stlaceni klavesy shift
                break

    #event handler
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #ukoncenie hry
            if score> high_score: # ulozi sa najvyssie dosiahnute skore
                high_score= score
                with open('score.txt','w') as file:
                    file.write(str(high_score))
            run= False
    
#update display window
    pygame.display.update()

pygame.quit()
