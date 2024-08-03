from data.modules.renderapi import getfonts,draw_button,drawRhomboid,center_text
from data.modules.bootstrap import getactivity,transitionprep,gamepath,version,getname,getimg,getcopyrighttext,setmsg,samplepath,notification
from data.modules.beatmap_processor import get_info,beatmap_count,beatmaplist,random_beatmap,getbackground
from data.modules.audio import get_pos,get_tick,inc_tick
from data.modules.settings import settingskeystore,getsetting,togset
from data.modules.gameplay import song_progress
from data.modules.songselect import prepare,resetdcursor,selected
from data.modules.card import main as card
from data.modules.onlineapi import getmystats,getsigned,getnotice
from tweener import *
import pygame,sys
from random import randint
from data.modules.colours import *
meid=0
wid=180
hei=149
scale=0.8
mdur=250
measetype=Easing.BOUNCE
mtext=('Play','Create','Browse','Leave'),('Solo','Multi','Back')
bladeani=[Tween(begin=0, end=101,duration=500,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
menupos=tuple([Tween(begin=0),0] for a in mtext[0])
fmove=[0 for a in mtext[0]]
moveid=[0 for a in mtext[0]]
pmove=[0 for a in mtext[0]]
osam=0
olds=0,0
def getflash():
    return flashscr
def main(screen,w,h):
    global moveid,pmove,fmove,menupos,tick,osam,olds,flashscr,bg,topbar,sysbutton,flashylights
    bpm=get_info('bpm')
    if not bpm:
        bpm=500
    flashylights=(1-((get_pos()/bpm)-get_tick()))
    if flashylights<0:
        flashylights=0
    elif flashylights>1:
        flashylights=1
    elif get_pos()<=-1:
        flashylights=0
    if settingskeystore['effects'] or getactivity() == 5:
        bgcolour=255*flashylights
    else:
        bgcolour=0
    if get_pos()//bpm>get_tick():
        inc_tick()
    if olds!=(w,h):
        olds=w,h
        flashscr=pygame.surface.Surface(olds)
        flashscr.set_alpha(10)
        bg=pygame.surface.Surface(olds)
        topbar=pygame.surface.Surface((olds[0],40))
        topbar.set_alpha(80)
    flashscr.fill((bgcolour,bgcolour,bgcolour))
    if getactivity()==1:
        if not bladeani[1] and getactivity()==1:
            bladeani[1]=1
            bladeani[0].start()    
        bladeani[0].update()
        mouse=pygame.mouse.get_pos()
        parallax = (mouse[0]/w*10)-5, (mouse[1]/h*10)-5
        bgs=getbackground(w,h)
        if getsetting('bgmm') and bgs and len(beatmaplist):
            bg.blit(bgs,parallax)
        else:
            bg.fill((maincolour[0][0],maincolour[0][1],maincolour[0][2]))
        #screen.blits(((bg,(0,0)),(flashscr,(0,0))))
        screen.blit(bg,(0,0))
        micon='logomini.png','edit.png','browse.png','exit.png'
        if version()=='0.0.0':
            gameverstr=''
        else:
            gameverstr=version()
        pygame.draw.rect(topbar,(0,0,0),pygame.Rect(0,0,w,40))
        screen.blit(topbar,(0,0))
        if beatmap_count():
            screen.blit(getfonts(0).render(get_info('songtitle'),True,(255,255,255)),(10,10))
        else:
            screen.blit(getfonts(0).render('Get Songs!! >w<',True,(255,255,255)),(10,10))
        ani=((100-bladeani[0].value)/100)
        bla=(ani*w)
        mmenu=[]
        notice=getnotice()
        if notice!='':
            #tmp = getfonts(0).render(notice,  True,  (0,0,0))
            #txtrect=tmp.get_rect()
            #pygame.draw.rect(screen,maincolour[1],pygame.Rect(w//2-(txtrect[2]//2)-10-parallax[0],h//2-170-parallax[1],txtrect[2]+20,50),border_radius=10)
            pygame.draw.rect(screen,(maincolour[1]),(0,h//2-90-parallax[1],w+10,32))
            #screen.blit(getfonts(0).render(notice,True,(255,255,255)),(10-parallax[0],h//2-85-parallax[1]))
            center_text(screen,notice,(10-parallax[0],h//2-90-parallax[1],w+10,30),'',(255,255,255))
        if getsigned():
            card(screen,(w//2-150-parallax[0],h//2+120-parallax[1]),accuracy=getmystats()[0],points=getmystats()[1],rank=getmystats()[2],score=getmystats()[3],level=getmystats()[4],username=getsetting('username'))
        mmenu = ((fmove[a-1]+(bla-parallax[0]+(w//2-((wid*scale)*(len(mtext[meid])/2))+((wid*scale)*(a-1))))-(moveid[a-1]//2)-pmove[a-1],h//2-(75*scale)-parallax[1],(wid*scale)+moveid[a-1],hei*scale) for a in range(1,len(mtext[meid])+1))
        drawRhomboid(screen,dcolour,bla-25-parallax[0],h//2-(76*scale)+1-parallax[1],w+80,hei*scale,26)
        tmenu=((w-(40*a),0,40,40) for a in range(1,4))
        button, highlight=draw_button(screen,mmenu,mtext[meid],isblade=1,return_hover=1,icon=micon,textoffset=(-10,25),iconoffset=(-7,-10))
        topbutton=draw_button(screen,tmenu,'',hidetext=1,icon=('settings.png','user.png','download.png'),border_radius=0)
        if version()[0]!='0.0.0':
            name=getname()
            bottomtext=name[0]+'/'+name[1]+' ('+version()[0]+')'
            col=255,255,255
        else:
            bottomtext='Development build'
            col=(255,255,0)
        c=getfonts(0).render(bottomtext,True,col)
        d=c.get_rect(center=pygame.Rect(w//2,h-35,0,0).center)
        screen.blit(c,(d[:2]))
        screen.blit(getfonts(1).render(getcopyrighttext(),True,(255,255,255)),(10,50))

## Progress bar for media
        if beatmap_count():
            if get_pos() >= eval(get_info('lengths'))[selected[1]]+1000:
                resetdcursor()
                tmp=random_beatmap()
                prepare(tmp[1])
            song_progress(screen,get_pos(),eval(get_info('lengths'))[selected[1]]+1000,w,h)

## Animation
        for a in range(0,len(mtext[0])):
            menupos[a][0].update()   
            moveid[a]=menupos[a][0].value
            if a!=len(menupos)-1:
                pmove[a]=menupos[a+1][0].value//2
            fmove[a]=menupos[a-1][0].value//2
            if highlight==a:
                if not menupos[a][1]:
                    menupos[a][0]=Tween(begin=moveid[a], end=20,duration=mdur,easing=measetype,easing_mode=EasingMode.OUT)
                    menupos[a][1]=1
                    menupos[a][0].start()
            elif highlight!=a:
                if menupos[a][1]:
                    menupos[a][0]=Tween(begin=moveid[a], end=0,duration=mdur,easing=measetype,easing_mode=EasingMode.OUT)
                    menupos[a][1]=0
                    menupos[a][0].start()

# MSG

        if highlight == 0:
            setmsg(' You have '+str(format(beatmap_count(),','))+' Songs ')
        elif highlight == 1 and meid:
            setmsg('Play with the world!')
        elif highlight == 1 and not meid:
            setmsg('Time to make beatmaps!')
        elif highlight == 2 and not meid:
            setmsg('Browse our catalog')
        elif highlight == 3 and not meid:
            setmsg('See ya next time~')
        else:
            setmsg('')
        if osam!=highlight:
            osam=highlight
            pygame.mixer.Sound(samplepath+'hover.wav').play()
## Input

        if button == 1:
            transitionprep(2)
        elif button == 2:
            notification('Error',desc='In construction!!')
            #transitionprep(3)
        elif button == 3:
            transitionprep(4)
        elif button == 4:
            transitionprep(-1)
        elif topbutton == 1:
            togset()
        elif topbutton == 2:
            transitionprep(7)
        elif topbutton == 3:
            transitionprep(8)
    else:
        bladeani[1]=0

    