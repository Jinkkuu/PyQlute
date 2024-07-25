import pygame,time,sys
from data.modules.renderapi import getfonts
from data.modules.colours import maincolour
def main(screen,pos,points=0,score=0,overidecolour=0,hidebg=0,level=0,rank=0,accuracy=69,username=None,mini=False):
    ticker=time.time()
    p=points
    r=rank
    points=format(points,',')
    rank = format(rank,',')
    level = format(level,',')
    score = format(score,',')
    if not overidecolour:
        blend=maincolour[5][0]-20,maincolour[5][1]-20,maincolour[5][2]-20
    else:
        blend=overidecolour
    if mini:
        height=50
    else:
        height=70
    if not hidebg:
        pygame.draw.rect(screen,maincolour[5],pygame.Rect(pos[0],pos[1],300,height),border_radius=10)
    if r>0 and p>0:
        t=getfonts(4).render(f'#{rank}',True,blend)
        rtl=t.get_rect()
        rtl=pos[0]+290-rtl[2],pos[1]+height-50
        screen.blit(t,rtl[:2])
        t=getfonts(1).render(f'Accuracy - {str(round(accuracy,2))}%',True,(255,255,255))
        rtl=t.get_rect()
        rtl=pos[0]+290-rtl[2],pos[1]+height-20
        screen.blit(getfonts(1).render(f'{points}pp',True,(255,255,255)),(pos[0]+10,pos[1]+30))
        screen.blit(t,rtl[:2])
        if not mini:
            screen.blit(getfonts(1).render(f'{score}',True,(255,255,255)),(pos[0]+10,pos[1]+50))
    screen.blit(getfonts(0).render(str(username),True,(255,255,255)),(pos[0]+10,pos[1]+5))