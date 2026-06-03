
# Ultimate Neon Pong with Audio Support
# Place these files in an assets folder beside this script:
# assets/bg_music.mp3
# assets/hit.wav
# assets/score.wav
# assets/win.wav

import pygame, sys, math, random, os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Neon Pong")
clock = pygame.time.Clock()

# Audio
hit_sound = score_sound = win_sound = None
try:
    hit_sound = pygame.mixer.Sound("assets/hit.wav")
    score_sound = pygame.mixer.Sound("assets/score.wav")
    win_sound = pygame.mixer.Sound("assets/win.wav")

    pygame.mixer.music.load("assets/bg_music.mp3")
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Audio load warning:", e)

BG=(5,5,15)
WHITE=(240,240,240)
CYAN=(0,220,255)
MAGENTA=(255,0,180)
GREEN=(0,255,150)

TITLE=pygame.font.SysFont("Arial",64,True)
FONT=pygame.font.SysFont("Arial",32)
SCORE=pygame.font.SysFont("Arial",56)

state="menu"
mode=None
winner=""

class Button:
    def __init__(self,x,y,w,h,text,color):
        self.r=pygame.Rect(x,y,w,h)
        self.text=text
        self.color=color
    def draw(self):
        pygame.draw.rect(screen,self.color,self.r,border_radius=10)
        t=FONT.render(self.text,True,WHITE)
        screen.blit(t,t.get_rect(center=self.r.center))
    def hit(self,pos):
        return self.r.collidepoint(pos)

single=Button(350,220,300,70,"Single Player",CYAN)
multi=Button(350,320,300,70,"Two Players",MAGENTA)
quitb=Button(350,420,300,70,"Quit",(220,70,70))

def play(s):
    try:
        if s: s.play()
    except:
        pass

def glow_rect(rect,color):
    for i in range(12,0,-4):
        surf=pygame.Surface((rect.w+i*2,rect.h+i*2),pygame.SRCALPHA)
        pygame.draw.rect(surf,(*color,max(3,35-i)),surf.get_rect(),border_radius=8)
        screen.blit(surf,(rect.x-i,rect.y-i))
    pygame.draw.rect(screen,color,rect,border_radius=6)

def glow_ball(rect):
    c=rect.center
    for r in range(18,4,-4):
        surf=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(surf,(255,255,255,max(2,30-r)),(r,r),r)
        screen.blit(surf,(c[0]-r,c[1]-r))
    pygame.draw.circle(screen,WHITE,c,rect.w//2)

def reset():
    global lp,rp,ball,bx,by,ls,rs
    lp=pygame.Rect(40,HEIGHT//2-50,15,100)
    rp=pygame.Rect(WIDTH-55,HEIGHT//2-50,15,100)
    ball=pygame.Rect(WIDTH//2-10,HEIGHT//2-10,20,20)
    bx,by=6,6
    ls=rs=0

def center_ball():
    global bx,by
    ball.center=(WIDTH//2,HEIGHT//2)
    bx=-bx
    by=random.choice([-6,6])

reset()

running=True
while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

        if state=="menu" and e.type==pygame.MOUSEBUTTONDOWN:
            if single.hit(e.pos):
                mode="single"; reset(); state="game"
            elif multi.hit(e.pos):
                mode="multi"; reset(); state="game"
            elif quitb.hit(e.pos):
                running=False

        elif state=="game" and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_ESCAPE:
                state="pause"
            if e.key==pygame.K_m:
                pygame.mixer.music.set_volume(0 if pygame.mixer.music.get_volume()>0 else 0.35)

        elif state=="pause" and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_ESCAPE: state="game"
            if e.key==pygame.K_q: state="menu"

        elif state=="over" and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_RETURN: state="menu"

    screen.fill(BG)

    for x in range(0,WIDTH,50):
        pygame.draw.line(screen,(10,10,30),(x,0),(x,HEIGHT))
    for y in range(0,HEIGHT,50):
        pygame.draw.line(screen,(10,10,30),(0,y),(WIDTH,y))

    if state=="menu":
        glow=int(180+75*math.sin(pygame.time.get_ticks()*0.005))
        t=TITLE.render("ULTIMATE NEON PONG",True,(0,glow,255))
        screen.blit(t,t.get_rect(center=(WIDTH//2,120)))
        single.draw(); multi.draw(); quitb.draw()

    elif state=="game":
        keys=pygame.key.get_pressed()
        if keys[pygame.K_w] and lp.top>0: lp.y-=8
        if keys[pygame.K_s] and lp.bottom<HEIGHT: lp.y+=8

        if mode=="single":
            if ball.centery<rp.centery: rp.y-=6
            elif ball.centery>rp.centery: rp.y+=6
        else:
            if keys[pygame.K_UP] and rp.top>0: rp.y-=8
            if keys[pygame.K_DOWN] and rp.bottom<HEIGHT: rp.y+=8

        ball.x+=bx; ball.y+=by

        if ball.top<=0 or ball.bottom>=HEIGHT:
            by=-by

        if ball.colliderect(lp):
            ball.left=lp.right
            bx=abs(bx)+0.2
            play(hit_sound)

        if ball.colliderect(rp):
            ball.right=rp.left
            bx=-(abs(bx)+0.2)
            play(hit_sound)

        if ball.left<=0:
            rs+=1
            play(score_sound)
            center_ball()

        if ball.right>=WIDTH:
            ls+=1
            play(score_sound)
            center_ball()

        if ls>=10:
            winner="PLAYER 1 WINS!"
            play(win_sound)
            state="over"

        if rs>=10:
            winner="AI WINS!" if mode=="single" else "PLAYER 2 WINS!"
            play(win_sound)
            state="over"

        for yy in range(0,HEIGHT,30):
            pygame.draw.rect(screen,(100,100,220),(WIDTH//2-2,yy,4,15))

        glow_rect(lp,CYAN)
        glow_rect(rp,MAGENTA)
        glow_ball(ball)

        screen.blit(SCORE.render(str(ls),True,CYAN),(WIDTH//4,20))
        screen.blit(SCORE.render(str(rs),True,MAGENTA),(WIDTH*3//4,20))

    elif state=="pause":
        t=TITLE.render("PAUSED",True,WHITE)
        screen.blit(t,t.get_rect(center=(WIDTH//2,250)))

    elif state=="over":
        t=TITLE.render(winner,True,GREEN)
        screen.blit(t,t.get_rect(center=(WIDTH//2,250)))
        m=FONT.render("Press ENTER",True,WHITE)
        screen.blit(m,m.get_rect(center=(WIDTH//2,330)))

    pygame.display.flip()

pygame.quit()
sys.exit()
