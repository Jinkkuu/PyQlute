from data.modules.bootstrap import getactivity,setactivity
import pygame
from data.modules.colours import maincolour
from data.modules.renderapi import getfonts,draw_button
from data.modules.gameplay import showplayfield
editprocess=1
def editmenu(screen,w,h):
    if getactivity() == 3:
        screen.fill((10,10,10))
        showplayfield(screen,(w//2,0))
        pygame.draw.rect(screen,maincolour[8],(0,0,w,60))
        screen.blit(getfonts(0).render('Create ('+str(editprocess)+'/3)',True,(255,255,255)),(20,20))
        draw_button(screen,((10,80,100,50),(10,140,100,50)),('Place','Select'))
        draw_button(screen,((w-110,80,100,50),(w-110,140,100,50),(w-110,200,100,50)),('Normal','Soft','Loud'))
