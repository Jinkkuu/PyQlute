from data.modules.bootstrap import getuserdata,getactivity,setmsg,transitionprep,gamever,gamename
from data.modules.renderapi import getfonts,draw_button
from data.modules.colours import maincolour
from data.modules.input import get_input
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
        'skin' : None,
        'discordrpc' : True,
        'screenshot_id' : 0,
        'hidegamehud' : 0,
        'master' : 100,
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
def controlsetup(screen,w,h):
    global sysbutton,cset
    if getactivity()==13:
        pygame.draw.rect(screen,(42,40,95),pygame.Rect(0,0,w,h))
        pygame.draw.rect(screen,maincolour[0],pygame.Rect(0,h-60,w,60))
        screen.blit(getfonts(2).render('Controls',True,(255,255,255)),(20,20))
        screen.blit(getfonts(0).render('Click the one you want to change',True,(255,255,255)),(20,20))
        sysbutton=draw_button(((-10,h-60,100,60),(w//2-160,h//2-80,80,80),(w//2-80,h//2-80,80,80),(w//2,h//2-80,80,80),(w//2+80,h//2-80,80,80),),('Back',settingskeystore['Key1'].upper(),settingskeystore['Key2'].upper(),settingskeystore['Key3'].upper(),settingskeystore['Key4'].upper()),border_radius=0,selected_button=cset+1)
def settingspage(screen,w,h):
    global setupid,fpsmode,setbutton,catbutton
    if getactivity()==6:
        if str(fpsmodes[fpsmode])!='1000':
            tmp=str(fpsmodes[fpsmode])
        else:
            tmp='Unlimited'
        if not settingskeystore['username']:
            user='Guest'
        else:
            user=settingskeystore['username']
        setuplist={'general': {'Leaderboards':settingskeystore['leaderboard'],'Effects':settingskeystore['effects'],'Save Replays':settingskeystore['sreplay'],'Enable BG':settingskeystore['bgmm'],'Controls':'->','Show FPS':settingskeystore['fpsmetre'],'Discord RPC':settingskeystore['discordrpc'],},'skinning':{'Change Skins':'->','Note Width':'->','Note Height':'->','Note Colour':'->','Background Colour':'->','HealthBar Colour':'->','Insanity Level':'->',},'audio':{'Hitsounds':settingskeystore['hitsound']},'graphics':{'FPS':tmp,'Fullscreen':settingskeystore['fullscreen']},'debug':{},'account':{'Username':user,'Medals':'->'}}
        setuplistpos=[]
        b=0
        screen.fill(maincolour[4])
        if setupid==5:
            screen.blit(getfonts(0).render('Game Name - '+str(gamename),True,(255,255,255)),(20,120+(23*0)))
            screen.blit(getfonts(0).render('Game Version - '+str(gamever),True,(255,255,255)),(20,120+(23*1)))
        else:
            setuptxt=[]
            for a in setuplist[setupcatagory[setupid-1].lower()]:
                b+=1
                poof=offset[1]+40
                if setupid==2:
                    posw=20
                else:
                    posw=w//2-110
                text=str(setuplist[setupcatagory[setupid-1].lower()][a])
                if '->' in text:
                    sp=' '
                else:
                    sp=' : ' 
                setuplistpos.append((posw,  poof+(50*b),  220,  33))
                setuptxt.append(a+sp+text)
            if len(setuptxt)<1:
                setbutton,sh=0,0
            else:
                setbutton,sh=draw_button(screen,(setuplistpos), (setuptxt),return_hover=1)
            if sh == 0 and setupid==4:
                setmsg('Changes how fast this game goes')
            elif sh == 1 and setupid==4:
                setmsg('Makes the Screen Fullscreen, what do you expect')
            elif sh == 1 and setupid==1:
                setmsg('Changes the Flashing Effect')
            elif sh == 0 and setupid==3:
                setmsg('Enable Hitsounds')
            elif sh == 0 and setupid==1:
                setmsg('Enable Leaderboards')
            elif sh == 2 and setupid==1:
                setmsg('Auto Save Replays')
            elif sh == 3 and setupid==1:
                setmsg("Show song's Background at the main menu")
            elif sh == 5 and setupid==1:
                setmsg("Shows in-game FPS")
            elif sh == 4 and setupid==1:
                setmsg('Change your controls for your gameplay')
            else:
                setmsg('')
        pygame.draw.rect(screen,maincolour[5],pygame.Rect(0,h-60,w,60))
        pygame.draw.rect(screen,maincolour[5],pygame.Rect(0,0,w,100))
        catbutton=draw_button(screen,(setupcatpos), (setupcatagory),selected_button=setupid,fonttype=1,border_radius=0)
        screen.blit(getfonts(2).render('Settings',True,(255,255,255)),offset)
        sysbutton=draw_button(screen,((-10,h-60,100,60),),('Back',),border_radius=0)
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
                if setbutton:
                    reloadsettings()
                if setbutton  ==  1 and setupid==4:
                    change=True
                    if fpsmode<1:
                        fpsmode=len(fpsmodes)-1
                    else:
                        fpsmode-=1
                    settingskeystore['fps']=fpsmodes[fpsmode]
                    reloadsettings()
                elif setbutton == 3 and setupid==1:
                    settingskeystore['sreplay']=not settingskeystore['sreplay']
                    reloadsettings()
                elif setbutton == 6 and setupid==1:
                    settingskeystore['fpsmetre']=not settingskeystore['fpsmetre']
                    reloadsettings()
                elif setbutton == 7 and setupid==1:
                    settingskeystore['discordrpc']=not settingskeystore['discordrpc']
                    reloadsettings()
                elif setbutton == 2 and setupid==4:
                  settingskeystore['fullscreen'] = not settingskeystore['fullscreen']
                  firstcom=False
                elif setbutton == 1 and setupid==3:
                  settingskeystore['hitsound'] = not settingskeystore['hitsound']
                elif setbutton == 1 and setupid==1:
                  settingskeystore['leaderboard'] = not settingskeystore['leaderboard']
                elif setbutton == 2 and setupid==1:
                  settingskeystore['effects'] = not settingskeystore['effects']
                elif setbutton == 4 and setupid==1:
                  settingskeystore['bgmm'] = not settingskeystore['bgmm']
                elif setbutton == 2 and setupid==6:
                    transitionprep(17)
                    sbid=0
                    shopscroll=0
                elif setbutton == 5 and setupid==1:
                    transitionprep(13)
                    cset=-1
                elif sysbutton:
                    transitionprep(1)
