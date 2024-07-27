from data.modules.bootstrap import getactivity,transitionprep,clockify
from data.modules.renderapi import getfonts
import pygame,time
testclock=time.time()+48680
popupcolour=(80,80,150)
def questoftheday(screen,w,h):
    if getactivity() == 10:
        screen.fill(popupcolour)
        screen.blit(getfonts(2).render('Quest of the Day',1,(255,255,255)),(10,10))
        screen.blit(getfonts(0).render('You have '+clockify((testclock-time.time())/0.001)+' to complete the Quest!',1,(255,255,255)),(10,60))


    