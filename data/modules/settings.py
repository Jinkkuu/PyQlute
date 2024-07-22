from data.modules.bootstrap import getuserdata,getactivity,setmsg,transitionprep,gamever,gamename
from data.modules.renderapi import getfonts,draw_button
from data.modules.colours import maincolour
from data.modules.input import get_input
from tweener import *
import json,os,pygame
def reloadsettings():
    tmp=open(getuserdata()+'settings', 'w')
    tmp.write(json.dumps(settingskeystore))
    tmp.close()
fpsmodes=[30,60,120,240,480,1000]
settingstemplate={
        'hitsound' : True,
        'leaderboard' : True,
        'fullscreen' : False,
        'effects' : True,
        'skinning' : True,
        'username' : None,
        'password' : None,
        'apiurl' : 'https://qlute.pxki.us.to/',
        'bgmm' : True,
        'sreplay':True,
        'fps' : 480,
        'Key1' : 'd',
        'Key2' : 'f',
        'Key3' : 'j',
        'Key4' : 'k',
        'Key5' : 's',
        'Key6' : 'l',
        'Key7' : 'a',
        'Key8' : ';',
        'skin' : None,
        'discordrpc' : True,
        'screenshot_id' : 0,
        'hidegamehud' : 0,
        'master' : 100,
        'classicmode' : False,
        'fpsmetre' : False
    }
setupid=1
setupcatagory=('General','Skinning','Audio','Graphics','Debug','Account')
setupcatpos=[]
catbutton=0
setbutton=0
b=0
for a in setupcatagory:
    setupcatpos.append((0+(100*b),80,100,20))
    b+=1
cset=0
offset=20,20
if os.path.isfile(getuserdata()+'settings'):
    print('Using SettingsV2...')
    settingskeystore=json.load(open(getuserdata()+'settings'))
    for a in settingstemplate:
        if not a in settingskeystore:
            settingskeystore[a]=settingstemplate[a]
            reloadsettings()
    print('Completed')
else:
    settingskeystore=settingstemplate
fpsmode=fpsmodes.index(settingskeystore['fps'])
def getsetting(value):
    try:
        return settingskeystore[value]
    except KeyError as err:
        print(err,'getsetting')
        return 0
def setsetting(value,changeto):
    try:
        settingskeystore[value]=changeto
        reloadsettings()
    except KeyError as err:
        print(err)
        return 0
setshow=0
def chkset():
    return setshow
def controlsetup(screen,w,h):
    global sysbutton,cset
    if getactivity()==13:
        pygame.draw.rect(screen,(42,40,95),pygame.Rect(0,0,w,h))
        pygame.draw.rect(screen,maincolour[0],pygame.Rect(0,h-60,w,60))
        screen.blit(getfonts(2).render('Controls',True,(255,255,255)),(20,20))
        screen.blit(getfonts(0).render('Click the one you want to change',True,(255,255,255)),(20,20))
        sysbutton=draw_button(((-10,h-60,100,60),(w//2-160,h//2-80,80,80),(w//2-80,h//2-80,80,80),(w//2,h//2-80,80,80),(w//2+80,h//2-80,80,80),),('Back',settingskeystore['Key1'].upper(),settingskeystore['Key2'].upper(),settingskeystore['Key3'].upper(),settingskeystore['Key4'].upper()),border_radius=0,selected_button=cset+1)

ctrl=0
obut=0
setani=Tween(begin=0, end=0,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT)
setani.start()
settingscroll=0
clickcol=(10,10,10),(150,150,255)
def checkbutton(screen,buttonpos,buttontext,buttonticked,title='Test'):
    screen.blit(getfonts(0).render(title,True,(210, 158, 255)),(10,buttonpos[0][1]-40))
    id=1
    clicked=0
    cid=0
    for text in enumerate(buttontext):
        #print(text)
        butt=buttonpos[text[0]]
        butt=butt[0],butt[1]
        tes=getfonts(1).render(text[1],True,(255,255,255))
        rect=tes.get_rect()
        tmp=buttonticked[text[0]]
        if tmp in (0,1):
            buttpos=pygame.Rect(rect[2]+20,buttonpos[text[0]][1]-2,35,rect[3])
        else:
            txt=getfonts(1).render(': '+tmp,True,(255,255,255))
            buttpos=txt.get_rect()[-1]
            buttpos=pygame.Rect(0,buttonpos[text[0]][1]-2,400,buttpos)
        mouse=pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(buttpos,mouse[0],mouse[1]):
            hover=20
            clickedid=id
        else:
            clickedid=0
            id+=1
            hover=0
        if tmp in (0,1):
            pygame.draw.rect(screen,(clickcol[tmp][0]+hover,clickcol[tmp][1]+hover,clickcol[tmp][2]),buttpos,border_radius=10)
        else:
            pygame.draw.rect(screen,(50+hover,50+hover,80+hover),buttpos)
            screen.blit(txt,(rect[2]+10,buttonpos[text[0]][1]))
        screen.blit(tes,butt)
        for event in get_input():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and clickedid:
                clicked=1
                cid=clickedid
    return cid,clicked
sh=0
sw=0
def togset():
    global setani,setshow
    setani=Tween(begin=setshow, end=not setshow,duration=200,easing=Easing.CUBIC,easing_mode=EasingMode.OUT)
    setani.start()
    setshow=not setshow
def settingspage(screen,w,h):
    global setupid,fpsmode,setbutton,catbutton,ctrl,obut,setshow,setani,settingscroll,setpage,sh,sw,blackout
    setani.update()
    if not "setpage" in globals() or sh!=h or sw!=w:
        print('changed')
        sh=h
        sw=w
        setpage=pygame.surface.Surface((400,h),pygame.SRCALPHA).convert()
        blackout=pygame.surface.Surface((w,h)).convert()
    if setani.value <= 0.99 and setani.value > 0.01:
        blackout.set_alpha(100*setani.value)
    if setani.value>0:
        if str(fpsmodes[fpsmode])!='1000':
            tmp=str(fpsmodes[fpsmode])
        else:
            tmp='Unlimited'
        if not settingskeystore['username']:
            user='Guest'
        else:
            user=settingskeystore['username']
        setpage.fill((50,50,80))
        setuplist={'general': {'Leaderboards':settingskeystore['leaderboard'],
                               'Save Replays':settingskeystore['sreplay'],
                               'Discord RPC':settingskeystore['discordrpc'],
                               },
                               'skinning':{},
                               'audio':{'Hitsounds':settingskeystore['hitsound']
                                        },
                               'graphics':{'FPS':tmp,
                                           'Fullscreen':settingskeystore['fullscreen'],
                                           'Enable BG':settingskeystore['bgmm'],
                                           'Effects':settingskeystore['effects'],
                                           'Show FPS':settingskeystore['fpsmetre'],
                                           },
                               'debug':{},
                               'account':{'You are ':user}}
        setpage.blit(getfonts(2).render('Settings',True,(255,255,255)),(10,10+settingscroll))
        tick=0
        suck=0
        suckt=0
        for setupid in range(0,len(setupcatagory)):
            tmp=setuplist[setupcatagory[setupid].lower()]
            if len(tmp):
                tmpt=[]
                tmpp=[]
                tmpc=[]
                for a in tmp:
                    tmpt.append(a)
                    tmpc.append(tmp[a])
                    tmpp.append((10,120+tick+settingscroll))
                    tick+=20
                tick+=50
                boobs,cid = checkbutton(setpage,tmpp,tmp,tmpc,title=setupcatagory[setupid])

                if cid:
                    bootid=suck+boobs
                    if bootid == 1:
                        settingskeystore['leaderboard'] = not settingskeystore['leaderboard']
                    elif bootid == 2:
                        settingskeystore['sreplay']=not settingskeystore['sreplay']
                    elif bootid == 3:
                        settingskeystore['discordrpc']=not settingskeystore['discordrpc']
                    elif bootid == 4:
                        settingskeystore['hitsound'] = not settingskeystore['hitsound']
                    elif bootid  ==  5:
                        change=True
                        if fpsmode<1:
                            fpsmode=len(fpsmodes)-1
                        else:
                            fpsmode-=1
                        settingskeystore['fps']=fpsmodes[fpsmode]
                    elif bootid == 6:
                        settingskeystore['fullscreen'] = not settingskeystore['fullscreen']
                    elif bootid == 7:
                        settingskeystore['bgmm'] = not settingskeystore['bgmm']
                    elif bootid == 8:
                        settingskeystore['effects'] = not settingskeystore['effects']
                    elif bootid == 9:
                        settingskeystore['fpsmetre']=not settingskeystore['fpsmetre']
                    if bootid:
                        reloadsettings()
                else:
                    suck+=len(tmpt)
                    suckt+=1
        sysbutton=draw_button(setpage,((10,h-70,100,60),),('Back',),border_radius=10)

        screen.blit(blackout,(0,0))
        screen.blit(setpage,(-400+(400*setani.value),0))
    for event in get_input():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl=1
            if event.key == pygame.K_ESCAPE and setshow:
                ctrl=1
                obut=1
            if event.key == pygame.K_o:
                obut=1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl=0
            if event.key == pygame.K_o:
                obut=0
    if ctrl and obut:
        togset()
        ctrl=0
        obut=0
## Input
        for event in get_input():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if catbutton and not catbutton==2:
                    setupid=catbutton
                elif catbutton==2: # will introduce a better version
                    pass
#                    transitionprep(11)
#                    sbid=skinid
#                    shopscroll=0

