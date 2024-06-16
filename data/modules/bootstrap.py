#!/usr/bin/python3
#
#    Just Beats! (Qlute)
#    2020-2024 Pxki Games (Formally known as ??)
#    (Using Slyph Engine, Tinyworld's Game Engine)
#
#
import random,re,json,zipfile,os
from random import randint
import time, sys, threading, requests, socket,hashlib,io
from tweener import *
nline='\n'
axe=0
gamename='Qlute'
gameeditions='stable','beta','canary','dev'
if not "gamever" in globals():
    gamever='0.0.0'
if not "gameedition" in globals() or not gameedition.isdigit():
    gameedition=gameeditions[-1]
else:
    gameedition=gameeditions[int(gameedition)]
sylphenginever=gamever
gameverspl=gamever.split('.')
bypass_multiplayer=1
isquest=0
gamepath=datapath+'beatmaps/'
samplepath=syspath+'samples/'
downpath=datapath+'downloads/'
replaypath=datapath+'replays/'
skinpath=datapath+'skins/'
fontpath=syspath+'fonts/'
username='Guest'
propath=datapath+'profiles/'
profilepath=propath+username+'/'
gameauthor='Pxki Games'
level=0
print('Starting Game...')
button_size_height=33
stop=0
rankdiff='Easy','Normal','Hard','Extra','Expert','>n<','Devil'
rankdiffc=(0,100,200),(0,200,50),(150,200,0),(200,50,0),(0,0,0),(150,0,150)
sa=time.time()
gametime=0
ismusic=0
paths=datapath,gamepath,propath,profilepath,downpath,replaypath,skinpath
prestart=1
reloaddatabase=1
vol=100
volvismo=0
volvisual=0
isonline=False
menunotice=''
speed=1
leaderboard=[]
hitcolour=((100,120,200),(100,200,100),(200,200,100),(200,100,100))
for a in paths:
    if not os.path.isdir(a):
        os.mkdir(a)
        print('Created', a.replace('./', ''))
if not os.path.isfile(skinpath+'README.txt'):
    s=open(skinpath+'README.txt','w')
    s.write('Please add your skins here!\nIf you want to reload the skin just press F3 <3')
    s.close()
keyspeed=6
keyspeedb=13360/keyspeed
getpoints=0
debugmode=False
fps=0
update=False
offset=20,20
beatsel=0
beatnowmusic=1
score=0
maxperf=0
betaperf=0
comboburst=1000
perfbom=0.075
diff=[]
diffmode=''
diffcon=0
bgcolour=0
perf=0
maxobjec=255
objecon=0
oldupdatetime=0
totscore=0
tick=0
combo=0
lastms=0
darkness=0
stripetime=[]
bgtime=time.time()
objects=[]
speedvel=[0,0]
modsen=[0,0,0,0,0,0,0,0,0,0]
scoremult=1
modshow=False
msg=''
totrank=0
prevrank=0
uptime=time.time()
totperf=0
totscore=0
totacc=0
oldstats=[0,0]
rankmodes=('Ranked',(100,200,100)),('Unranked',(200,100,100)),('Special',(200,200,100)),('Loading...',(200,200,200)),

pygame.init()
fontname={'default':resource_path(fontpath+'default.ttf'),'bold':resource_path(fontpath+'defaultbold.ttf')}
clock=pygame.time.Clock()
activity=0
select=False
cross=[0,0]
crossboard=0
realid='' 
firstcom=False
combotime=0
maxplay=50
menuback=0
backspeed=1
replaymen=0
beka='None'
actto=activity
transb=0
transa=0
voltime=0
#tmp!!!!
msgx=0
messagetime=0
change=False
colorstep = 0
loaded=[]
ama=0
bars=[0,0,0,0,0,0,0,0]
t=''
miss=0
go=False
hits=[0,0,0,0]
#hitperfect=keymap[0][1]
#hitperfect=keymap[0][1]
last=0
ismulti=False # Enabling this would tell the game your in a multiplayer session
keys=[0,0,0,0]
keyslight=[Tween(begin=0),Tween(begin=0),Tween(begin=0),Tween(begin=0)]
pos=(64,192,320,448)
tip=0
sre=0
crox=[]
delta=0
mainurl='https://dev.catboy.best'
beatmapapi=mainurl+'/api/v2/'
beattitle=None
medals=[]
medals_name=[]
countersp=0
#def print(txt):
#    logbox.append((txt,time.time()))
drawtime=0.0000001
kiai=0
notemsg=['','']
noteani=[Tween(begin=0, end=100,duration=150,easing=Easing.CUBIC,easing_mode=EasingMode.OUT,boomerang=True),0]
notemaxh=1
useroverlay=0
upd=0
issubmiting=0
menupos=[]
mdur=250
measetype=Easing.BOUNCE
multilist=[]
multitime=0
for a in range(1,len(mtext[meid])+1):
    menupos.append([Tween(begin=0),0])
hittext='PERFECT!','GREAT','MEH','MISS'
hitcolour=(100, 120, 200),(100, 200, 100),(200, 200, 100),(200, 100, 100)
preparedmap=0
def notification(title,desc=''):
    global noteani,notemsg
    if os.path.isfile(samplepath+'notify.wav'):
        pygame.mixer.Sound(samplepath+'notify.wav').play()
    notemsg=[title,desc]
    noteani=[Tween(begin=0, end=notemaxh,duration=500,easing=Easing.CUBIC,easing_mode=EasingMode.OUT,boomerang=True),0]
    noteani[0].start()
def main():
    global fps, activity,preparedmap,beatnowmusic,change,upd,noteani,voltime,delta,trans,volvisual,volvismo,notemsg,flashylights,mtext, ingame, screen, settingskeystore,reloaddatabase,totrank, debugmode,sa,bgcolour,tick,scale,size,cardsize,bgtime,replaymen,allowed,posmouse,drawtime,scoremult,msg
    if change:
        reloadsettings()
        change=0
    for a in menupos:
        try:
            a[0].update()
        except Exception as err:
            print(err,time.time())
    if gameedition!=gameeditions[0]:
        gs='/'+gameedition
    else:
        gs=''
    if preparedmap and activity==4:
        beatnowmusic=1
        preparedmap=0
    msg=''
    if beattitle!=None and activity==4:
        alttitle=beattitle
    else:
        alttitle=''
    if gamever=='0.0.0':
        gameverstr=''
    else:
        gameverstr=gamever
    pygame.display.set_caption(gamename+gs+' '+gameverstr+' '+alttitle)
    if not firstcom:
        pygame.display.set_icon(programIcon)
    if activity in (9,10):
        pygame.mouse.set_visible(True)
    else:
        pygame.mouse.set_visible(False)
    update=time.time()
    posmouse=pygame.mouse.get_pos()
#    if modsen[0]:
#        scoremult=1

    if time.time()-sa>0.1:
        sa=time.time()
        fps=int(clock.get_fps())
    allowed=[0,1,2,3,5,6,7,8,11,12,13,14,15,16,17]
    upd=time.time()
    fullscreenchk()
    size=60
    scale=(w/400)
    if scale>=2:
        scale=2
    cardsize=int(300*scale)
    if activity==2:
        ingame=True
    else:
        ingame=False
    debugmode=settingskeystore['fpsmetre']

    if "bpm" in globals() and "beatmaps" in globals():
        if activity in allowed or kiai:
            if beatmaps!=0:
                if not activity in (3,7):
                    clear((maxt(bgdefaultcolour[0],bgcolour),maxt(bgdefaultcolour[1],bgcolour),maxt(bgdefaultcolour[2],bgcolour)))
                else:
                    clear((maxt(20,bgcolour),maxt(20,bgcolour),maxt(20,bgcolour)))
            else:
                clear(bgdefaultcolour)
            flashylights=(1-((gametime/bpm)-tick))
            if flashylights<0:
                flashylights=0
            elif flashylights>1:
                flashylights=1
            elif gametime<=-1:
                flashylights=0
            if settingskeystore['effects']:
                bgcolour=30*flashylights
            else:
                bgcolour=0
        if gametime//bpm>tick:
            tick+=1
    for a in os.listdir(downpath):
        if a.endswith('.osz'):
            if not os.path.isdir(gamepath+a.replace('.osz','')):
                os.mkdir(gamepath+a.replace('.osz',''))
                with zipfile.ZipFile(downpath+a, 'r') as zip_ref:
                    zip_ref.extractall(gamepath+a.replace('.osz','/'))
                    reloaddatabase=1
                notification('Beatmap Imported',desc=a)
            os.remove(downpath+a)
    if totrank<1:
        totrank=1
    get_input()
    beatmapload()
    logo()
    mainmenu()
    beatres()
    settingspage()
    beatmenu()
    customization()
    medalscreen()
    shopdirect()
    gameedit()
    loginscreen()
    controlsetup()
    downloads()
    multiplayer()
    if activity==-1:
        stopnow()
    if useroverlay:
        render('rect', arg=((0,-15,w,h//2), (60,60,60), False), borderradius=15)
        posy=10
        for a in range(1,25):
            posx=10+(310*(a-1))
            if posx>=w:
                posy+=90
            print_card(totperf,totscore,'aqua'+str(a),(posx,posy),a)
    try:
        game()
    except Exception as error:
        notification('Error!!',desc=error)
        transitionprep(3)
    if not notemsg[0]=='':
        sh=0
        sw=0
        for a in range(1,3):
            tmp = fonts[a-1].render(str(notemsg[a-1]),  True,  (0,0,0))
            txtrect=tmp.get_rect()
            if txtrect[2]+20>sw:
                sw+=txtrect[2]+20
            sh+=txtrect[3]+30
        notepos=w//2-(sw//2),(noteani[0].value*120)-100,sw,sh
        fcolor=(forepallete[0]*noteani[0].value,forepallete[1]*noteani[0].value,forepallete[2]*noteani[0].value)
        render('rect', arg=(notepos, (noteani[0].value*92,noteani[0].value*90,noteani[0].value*145), False), borderradius=15)
        render('text', arg=((0,0), fcolor, False,'center'),text=notemsg[0],relative=(notepos[0],notepos[1]+15,notepos[2],10))
        render('text', arg=((0,0), fcolor, False,'center','min'),text=notemsg[1],relative=(notepos[0],notepos[1]+20,notepos[2],notepos[3]-20))
        if noteani[0].value==notemaxh and not noteani[1]:
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
    if msg!='':
        tmp=(posmouse[0]+15,posmouse[1]+15,25,25)
        render('text',text=msg,arg=((tmp[0],tmp[1]),forepallete,'min','tooltip'))
        msg=''
    trans=1-transani[0].value
    render('rect', arg=((w*trans,0,w,h//2), hcol[0], False))
    render('rect', arg=((w*-trans,h//2,w,h//2), hcol[1], False))
    if actto==-1:
        render('text',text='See you next time~',arg=((0,0),forepallete,'grade','center'),relative=(w*trans,0,w,h-60))
    elif actto and transani[1]:
        rec=icons['logo.png'].get_rect(center=pygame.Rect(w*trans,0,w,h).center)
        screen.blit(icons['logo.png'],(rec[0],rec[1]))
    if transani[1]:
        transani[0].update()
        if transani[0].value==1:
            activity=actto
        elif transani[0].value==0:
            transani[1]=0
    if activity==1:
        of=35
    else:
        of=0
    volvisual=volani.value
    if int(volvisual)>int(vol) or int(volvisual)<int(vol):
        volani.update()
        v=1
    else:
        v=0
    if v:
        voltime=time.time()
    if not int(time.time()-voltime)>1:
        volpos=(20, h//2-100, 20, 200)
        render('rect', arg=((-15,h//2-105,115,210), (60,60,100), False), borderradius=15)
        render('rect', arg=(volpos, (20,20,20), False), borderradius=15)
        render('rect', arg=((volpos[0],volpos[1]+1+volpos[3]-((volvisual*0.01)*volpos[3]),volpos[2],(volvisual*0.01)*volpos[3]), (168*(volvisual*0.01), 232*(volvisual*0.01), 255*(volvisual*0.01)), False), borderradius=15)
        render('text',text=str(int(volvisual))+'%',arg=((0,0),forepallete,'center'),relative=(volpos[0]+50,volpos[1],0,volpos[3]))
    if debugmode:
        updatetime=(time.time()-upd)/0.001
        if updatetime>=10:
            fpscolour=(150,50,50)
        else:
            fpscolour=(50,150,50)
        render('rect', arg=((w-98, of+17, 110, 45), (fpscolour), False), borderradius=10)
        render('text', text=f'{fps} fps', arg=((w - 120, 23), forepallete, 'center'), relative=(w - 107, of + 20, 120, 20))
        render('text', text=f'{str(round(updatetime,2))}ms', arg=((w - 120, 43), forepallete, 'center'), relative=(w - 107, of + 40, 120, 20))        #render('text',text='TICK:'+str(tick)+'/'+str(gametime//bpm)+'/'+str(gametime)+'/'+str(bpm),arg=((20, 43),forepallete))
        #render('rect', arg=((5, 5, struct, 5), (0,255,0), False), borderradius=10)
#    x=0
#    for a in logbox[::-1][:10]:
#        if time.time()-a[1]>4:
#            logbox.remove(a)
#        render('rect', arg=((10, 10+(60*x), 150, 50), (20,20,20), False), borderradius=10)
#        render('text', text=a[0], arg=((0,0), forepallete, 'center'), relative=(10, 10+(60*x), 150, 50))
#        x+=1
    #print((time.time()-gametime)/0.001)
    if activity in allowed:
        if 'cursor.png' in icons:
            rec=icons['cursor.png'].get_rect()
            cen=rec[2]//2,rec[3]//2
            screen.blit(icons['cursor.png'],(posmouse[0]-cen[0],posmouse[1]-cen[1]))
        else:
            render('rect', arg=((posmouse[0]-10,posmouse[1]-10,20,20), (102, 155, 212), True),borderradius=20)
#    if not (posmouse[0],posmouse[1]) in crox:
#        crox.append((posmouse[0],posmouse[1]))
    pygame.display.flip()
    drawtime=clock.tick(fpsmodes[fpsmode])/1000
    delta=drawtime
    #print(drawtime)
nettick=0
timetaken=0
welcometext='Welcome to '+str(gamename)
logbox=[('Started Engine',time.time())]
def check_gameversion():
    ver=requests.get('https://github.com/Jinkkuu/PyQlute/releases/latest/download/RELEASE',timeout=10).text.rstrip('\n') # type: ignore
    if gamever!=ver and gamever!='0.0.0':
        notification('Notice',desc='Qlute '+str(ver)+' is out!, check on itch.io to update!')
def reloadicons():
    global skins,icons,skinid,hcol
    icons={}
    skins=[]
    skinid=0
    custom=0
    for a in os.listdir(skinpath):
        if os.path.isdir(skinpath+a):
            skins.append(a)
    if settingskeystore['skin'] and settingskeystore['skin'] in skins:
        currentskin=skinpath+settingskeystore['skin']+'/'
        skinid=skins.index(settingskeystore['skin'])
        if os.path.isfile(currentskin+'skin.cfg'):
            custom=1
            for a in open(currentskin+'skin.cfg').read().split('\n'):
                entry=a.split(':')
                if entry[0]=='colour':
                    hcol=eval(entry[1])
    else:
        currentskin=None
    if not custom:
        hcol=(62,60,115),(42,40,95),(22,20,75),(82,80,135)
    for pa in (resource_path(syspath+'icons/'),currentskin):
        if pa:
            for a in os.listdir(pa):
                try:
                    if os.path.isfile(pa+a):
                        icons[a]=(pygame.image.load(resource_path(pa+a))) # Icons!
                except Exception:
                    pass
    
def gamesession():
    while True:
        main()
if os.path.isfile(datapath+'.developer'):
    modsen[0]=1 # Automatically enables Auto Mod
if __name__  ==  "__main__":
    try:
        if os.path.isfile(datapath+'devsettings'):
            devset=open(datapath+'devsettings').read().split('\n')
            for a in devset:
                amp=a.split('=')
                if a[0][0]!='#':
                    if amp[0]=='apiurl':
                        apiurl=amp[1]
                    elif amp[0]=='username':
                        username=amp[1]
                    elif amp[0]=='vol':
                        vol=int(amp[1])
                    elif amp[0]=='welcometext':
                        welcometext=amp[1]
        if prestart:
            logotime=time.time()
        greph=[]
        for a in modsen:
            greph.append(randint(1,2)-1)
        reloadicons()
        micon=(icons['logomini.png'],icons['edit.png'],icons['browse.png'],icons['exit.png']),(icons['user.png'],icons['online.png'],icons['exit.png'],)
        programIcon = pygame.image.load(resource_path(syspath+'icon.png'))
        threading.Thread(target=ondemand).start()
        threading.Thread(target=check_gameversion).start()
        #threading.Thread(target=loginwindow).start()
        #for a in range(1,3):
            #threading.Thread(target=gamesession).start(
        while 1:
            if stop:
                sys.exit()
            main()
    except Exception as error:
        crash(str(error))
