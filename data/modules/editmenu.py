from data.modules.bootstrap import getactivity,setactivity,getimg,clockify
import pygame
from data.modules.colours import maincolour
from data.modules.renderapi import getfonts,draw_button
from data.modules.gameplay import showplayfield,pos
from data.modules.input import get_input
edittmp=[]
editmode=1
ti=0
def editmenu(screen,w,h):
    global ti
    if getactivity() == 3:
        mouse=pygame.mouse.get_pos()
        screen.fill((10,10,10))
        showplayfield(screen,(w//2,0))
        pygame.draw.rect(screen,maincolour[8],(0,0,w,60))
        screen.blit(getfonts(0).render('Create',True,(255,255,255)),(20,20))
        draw_button(screen,((10,80,100,50),(10,140,100,50)),('Place','Select'))
        draw_button(screen,((w-110,80,100,50),(w-110,140,100,50),(w-110,200,100,50)),('Normal','Soft','Loud'))
        blockpos = ti+h-mouse[1]
        pygame.draw.rect(screen,(50,50,50),(0,h-30,w,30))
        screen.blit(getfonts(0).render(clockify(ti),True,(255,255,255)),(10,h-25))
        for id in range(0,4):
            pou = pygame.Rect(w//2+(100*id)-200,mouse[1],100,30)
            if pygame.Rect.collidepoint(pou,mouse[0],mouse[1]):
                pygame.draw.rect(screen,(255,255,255),pou)
                screen.blit(getfonts(0).render('- '+clockify(blockpos),True,(255,255,255)),(w//2+210,mouse[1]))
                break
        for ob in edittmp:
            block=int(ti-int(ob[1])+h)
            bar=getimg('note.png')
            if bar:
                keyoffset=bar.get_rect()[3]
                screen.blit(bar,(w//2+(100*ob[0])-200,block-keyoffset))
    #        else:
    #            pygame.draw.rect(screen,notecolour[0],(fieldpos[0]-((keymap[0][2]*getkeycount()//2))+keymap[ob[1]][0],block-keymap[0][3],keymap[0][2],keymap[0][3]))
        for event in get_input():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    edittmp.append((id,blockpos))
                elif event.button == 4:
                    ti-=100
                    print(ti)
                elif event.button == 5:
                    ti+=100
            
            
