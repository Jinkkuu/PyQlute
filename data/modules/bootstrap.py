#
#    Qlute (Your Keys / Your Rhythm!)
#    2020-2024 Jinkku XD
#    (Using Mondeta Engine, Better Game Engine)
#
gamename='Qlute'
gameeditions='stable','beta','canary','dev'
gameauthor='Jinkku'
from tweener import *
import os,pygame,zipfile,time,gc
from data.modules.colours import maincolour
gc.enable()
def resource_path(relative_path):
    from os.path import abspath, join
    import sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)
def getuserdata(): # Get Userdata
    import os
    return os.path.expanduser('~')+'/.qlute/'
def getsysdata(): # Get Internal Data
    return resource_path('data/')
if os.path.isfile(getsysdata()+'.version'):
    gamever=open(getsysdata()+'.version').read().rstrip("\n")
else:
    gamever='0.0.0'
if os.path.isfile(getsysdata()+'.edition'):
    gameedition=gameeditions[int(open(getsysdata()+'.edition').read().rstrip("\n"))]
else:
    gameedition=gameeditions[-1]
print(gamename+'/'+str(gameedition),gamever) # Prints Game and version
activity=0
stop=0
def stopnow():
    global stop
    stop=1
def getstop():
    return stop
def getactivity():
    return activity
def setactivity(value):
    global activity,transani
    activity=value
def transitionprep(act):
    global transani,actto
    actto=act
    transani[1]=1
    transani[0].start()
def getact():
    return actto
def getname():
    return gamename,gameedition
def version():
    return gamever,gamever.split('.')
def reloadimg(): # This reloads the images from the game
    import os
    import pygame.image
    img={}
    for a in os.listdir(getsysdata()+'images/'):
        img[a]=pygame.image.load(getsysdata()+'images/'+a).convert_alpha()
    return img
def timeform(t):
    if t==None:
        return 'Never Played'
    if t>=31536000:
        x=int(t//31536000)
        fix='yr'
    elif t>=2630000:
        fix='mn'
        x=int(t//2630000)
    elif t>=86400:
        x=int(t//86400)
        fix='d'
    elif t>=3600:
        x=int(t//3600)
        fix='h'
    elif t>=60:
        x=int(t//60)
        fix='m'
    elif t<60:
        x=int(t)
        fix='s'
    return str(x)+fix

def getimg(value):
    try:
        return img[value]
    except KeyError:
        return None

gamepath=getuserdata()+'beatmaps/'
samplepath=getsysdata()+'samples/'
downpath=getuserdata()+'downloads/'
replaypath=getuserdata()+'replays/'
skinpath=getuserdata()+'skins/'
fontpath=getsysdata()+'fonts/'
screenshotfolder=getuserdata()+'screenshots/'
paths=getuserdata(),gamepath,downpath,replaypath,skinpath,screenshotfolder
msg=''
for a in paths:
    if not os.path.isdir(a):
        os.mkdir(a)
        print('Created', a.replace('./', ''))
def setmsg(value):
    global msg
    msg=value
def clockify(clo):
    clo/=1000
    minraw=int(clo/60)
    if minraw>98:
        minraw=99
    seco=int(clo-(60*minraw))
    if seco<0:
        pre='-'
        seco=-seco
    else:
        pre=''
    min="{:02d}".format(int(minraw))
    sec="{:02d}".format(seco)
    return pre+str(min)+':'+str(sec)
def sify(val1,val2):
    if val1>1:
        return val2+'s'
    else:
        return val2
def getcopyrighttext():
    return gameauthor+' 2023-2024'
def scrollbar(screen,startpos,endsize,search=3,length=5,colour=None):
    if not colour:
        colour=maincolour[2]
    try:
        t=-20
        t=(search/(length))*(endsize[1])
        pygame.draw.rect(screen,maincolour[1],pygame.Rect(startpos[0],startpos[1],endsize[0],endsize[1]))
        pygame.draw.rect(screen,colour,pygame.Rect(startpos[0],startpos[1]-t,endsize[0],endsize[1]//length))
    except Exception:
        pass
def getscreen():
    return screen.get_width(),screen.get_height()

notemsg=['','']
noteani=[Tween(begin=0, end=1,duration=150,easing=Easing.CUBIC,easing_mode=EasingMode.OUT,boomerang=True),0]
## Notifications prestart
vol=100
volvisual=0
def volchg(t):
    global vol,voltime,volani
    from data.modules.settings import setsetting
    voltime=time.time()+1
    step=5
    if vol<100 and t:
        volani=Tween(begin=vol, end=vol+step,duration=250,easing=Easing.CUBIC,easing_mode=EasingMode.OUT)
        volani.start()
        vol+=step
    elif vol>0 and not t:
        volani=Tween(begin=vol, end=vol-step,duration=250,easing=Easing.CUBIC,easing_mode=EasingMode.OUT)
        volani.start()
        vol-=step
    setsetting('master',vol)

def notification(title,desc=''):
    global noteani,notemsg
    if os.path.isfile(samplepath+'notify.wav'):
        pygame.mixer.Sound(samplepath+'notify.wav').play()
    notemsg=[title,desc]
    noteani=[Tween(begin=0, end=1,duration=500,easing=Easing.CUBIC,easing_mode=EasingMode.OUT,boomerang=True),0]
    noteani[0].start()
def main():
    global transani,img,screen,notemsg,vol,volani,volvisual
    import data.modules.settings as settings
    import data.modules.renderapi as renderapi
    from data.modules.mainmenu import main as mainmenu
    from data.modules.songselect import main as songselect
    from data.modules.accountpage import loginscreen
    from data.modules.songselect import ecross,prepare
    from data.modules.gameplay import main as gameplay
    from data.modules.resultsscreen import beatres
    from data.modules.shopscreen import shopdirect,downloads
    from data.modules.beatmap_processor import beatmaplist,random_beatmap,addbeatmap
    import data.modules.audio as audio
    import time,threading
    userdata = getuserdata()
    sysdata = getsysdata()
    screen=renderapi.initscreen()
    pygame.mouse.set_visible(False)
    from data.modules.input import main as poll
    from data.modules.input import get_input
    from data.modules.onlineapi import ondemand
    clock=pygame.time.Clock()
    fps=1
    fpsl=[]
    upl=[]
    img=reloadimg()
    threading.Thread(target=ondemand).start()
    if len(beatmaplist):
        tmp=random_beatmap()
        prepare(list(beatmaplist.keys()).index(tmp['songtitle']))
        del tmp
    transani=[Tween(begin=0, end=1,duration=150*2,easing=Easing.CUBIC,easing_mode=EasingMode.OUT,boomerang=True),0] # Animation for transitioning to another activity
    goaway = renderapi.getfonts(2).render('See you next time~',True,(255,255,255))
    focused=1
    vol=settings.getsetting('master')
    volani=Tween(begin=volvisual, end=vol,duration=250,easing=Easing.CUBIC,easing_mode=EasingMode.OUT)
    volani.start()
    while 1:
        upd=time.time()
        poll()
        for a in os.listdir(downpath):
            try:
                if a.endswith('.osz'):
                    print(a)
                    if not os.path.isdir(gamepath+a.replace('.osz','')):
                        os.mkdir(gamepath+a.replace('.osz',''))
                        with zipfile.ZipFile(downpath+a, 'r') as zip_ref:
                            zip_ref.extractall(gamepath+a.replace('.osz','/'))
                            addbeatmap(a.replace('.osz',''),save=1)
                        notification('Beatmap Imported',desc=a)
                    os.remove(downpath+a)
            except Exception:
                pass
        if focused:
            disactivity=settings.getsetting('fps')
        else:
            disactivity=30
        w=screen.get_width()
        h=screen.get_height()
        for event in get_input():
            if event.type == pygame.QUIT:
                transitionprep(-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mixer.Sound(samplepath+'click.wav').play()
            if event.type == pygame.WINDOWFOCUSGAINED:
                focused=1
            if event.type == pygame.WINDOWFOCUSLOST:
                focused=0
            if event.type == pygame.KEYDOWN:
                if event.key  ==  pygame.K_MINUS:
                    volchg(0)
                elif event.key  ==  pygame.K_EQUALS:
                    volchg(1)
                elif event.key == pygame.K_F12:
                    sub = screen.subsurface(pygame.Rect(0,0,w,h))
                    scid=settings.getsetting('screenshot_id')
                    pygame.image.save(sub, screenshotfolder+'screenshot_'+str(scid)+'.jpg')
                    notification('Screenshot Saved',desc='Saved as screenshot_'+str(scid)+'.jpg')
                    settings.setsetting('screenshot_id',scid+1)
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_F5:
                    settings.setsetting('fpsmetre',not settings.getsetting('fpsmetre'))
        mainmenu(screen,w,h)
        songselect(screen,w,h)
        try:
            gameplay(screen,w,h)
        except Exception as err:
            setactivity(2)
            notification('Game Crashed',desc=err)
        beatres(screen,w,h)
        shopdirect(screen,w,h)
        downloads(screen,w,h)
        loginscreen(screen,w,h)
        settings.settingspage(screen,w,h)
        if activity==-1:
            stopnow()
            exit()
        elif not activity:
            transitionprep(1)
        if transani[1]:
            transani[0].update()
            if transani[0].value==1:
                setactivity(actto)
            elif transani[0].value==0:
                transani[1]=0
        trans=1-transani[0].value
        pygame.draw.rect(screen,maincolour[2],pygame.Rect(w*trans,0,w,h//2))
        pygame.draw.rect(screen,maincolour[1],pygame.Rect(w*-trans,h//2,w,h//2))
        if actto==-1:
            out = goaway.get_rect(center=pygame.Rect(w*trans,0,w,h-60).center)
            screen.blit(goaway,(out[:2]))
        elif actto and transani[1]:
            rec=getimg('logo.png').get_rect(center=pygame.Rect(w*trans,0,w,h).center)
            screen.blit(getimg('logo.png'),(rec[0],rec[1]))
        volvisual=volani.value
        if int(volvisual)>int(vol) or int(volvisual)<int(vol):
            volani.update()
            v=1
        else:
            v=0
        if v:
            voltime=time.time()
        if not int(time.time()-voltime)>1:
            pygame.mixer.music.set_volume(0.8*(volvisual*0.01))
            volpos=(20, h//2-100, 20, 200)
            pygame.draw.rect(screen,(60,60,100),(-15,h//2-105,115,210),border_radius=15)
            pygame.draw.rect(screen,(20,20,20),volpos,border_radius=15)
            pygame.draw.rect(screen,(168*(volvisual*0.01), 232*(volvisual*0.01), 255*(volvisual*0.01)),(volpos[0],volpos[1]+1+volpos[3]-((volvisual*0.01)*volpos[3]),volpos[2],(volvisual*0.01)*volpos[3]),border_radius=15)
            renderapi.center_text(screen,str(int(volvisual))+'%',(volpos[0]+50,volpos[1],0,volpos[3]))
        mouse=pygame.mouse.get_pos()
        rec=getimg('cursor.png').get_rect()
        if len(msg):
            tmp=renderapi.getfonts(1).render(msg,1,(255,255,255))
            txtrect=tmp.get_rect()
            pygame.draw.rect(screen,(50,50,50),pygame.Rect(mouse[0]+rec[2]+5,mouse[1]+rec[3]+5,txtrect[2]+4,txtrect[3]+4),border_radius=5)
            screen.blit(tmp,(mouse[0]+rec[2]+8,mouse[1]+rec[3]+8))
            setmsg('')
        if not notemsg[0]=='':
            sh=0
            sw=0
            for a in range(1,3):
                tmp = renderapi.getfonts(a-1).render(str(notemsg[a-1]),  True,  (0,0,0))
                txtrect=tmp.get_rect()
                if txtrect[2]+20>sw:
                    sw+=(txtrect[2]+20)-sw
                sh+=txtrect[3]+30
            notepos=w//2-(sw//2),(noteani[0].value*120)-100,sw,sh
            fcolor=(255*noteani[0].value,255*noteani[0].value,255*noteani[0].value)
            pygame.draw.rect(screen,(noteani[0].value*92,noteani[0].value*90,noteani[0].value*145),notepos,border_radius=10)
            renderapi.center_text(screen,notemsg[0],(notepos[0],notepos[1]+15,notepos[2],10),colour=fcolor)
            renderapi.center_text(screen,notemsg[1],(notepos[0],notepos[1]+20,notepos[2],notepos[3]-20),type='min',colour=fcolor)
            if noteani[0].value==1 and not noteani[1]:
                if noteani[1]==0:
                    noteani[1]=time.time()
                noteani[0].pause()
            elif noteani[1]!=0 and time.time()-noteani[1]>3:
                noteani[0].resume()
                if noteani[0].value==0:
                    noteani[0].pause()
                    notemsg=['','']
                    noteani[1]=0
        noteani[0].update()
#        x=0
#        for a in maincolour:
#            pygame.draw.rect(screen,a,(20*x,100,20,20))
#            x+=1



        screen.blit(getimg('cursor.png'),(mouse[0],mouse[1]))
        if settings.getsetting('fpsmetre'):
            fps=0
            updatetime=0
            if len(upl)+1<300:
                upl.append((time.time()-upd)/0.001)
            else:
                upl=upl[100:]
            if len(fpsl)+1<300:
                fpsl.append(int(clock.get_fps()))
            else:
                fpsl=fpsl[100:]
            for a in upl:
                updatetime+=a
            updatetime=updatetime/len(upl)
            for a in fpsl:
                fps+=a
            fps=int(fps/len(fpsl))
            #updatetime=(time.time()-upd)/0.001
            if updatetime>=10:
                fpscolour=(150,50,50)
            else:
                fpscolour=(50,150,50)
            pygame.draw.rect(screen,fpscolour,pygame.Rect(w-98, 45, 98, 45),border_bottom_left_radius=10,border_top_left_radius=10)
            screen.blit(renderapi.getfonts(0).render(f'{fps} fps',True,(255,255,255)),(w - 90, 48))
            screen.blit(renderapi.getfonts(0).render(f'{round(updatetime,2)}ms',True,(255,255,255)),(w - 90, 68))
        drawtime=clock.tick(disactivity)/1000
        pygame.display.update()