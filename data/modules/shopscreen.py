import threading,pygame,io,requests,json
from data.modules.bootstrap import getactivity,transitionprep,scrollbar,notification,clockify
from data.modules.beatmap_processor import getpoint,rankmodes
from data.modules.colours import maincolour
from data.modules.input import get_input
from data.modules.onlineapi import downloadmap,getqueue
from data.modules.renderapi import getfonts,draw_button,textbox,center_text
from tweener import *
mainurl='https://catboy.best'
beatmapapi=mainurl+'/api/'
shopref=1
sbt=[]
serr=0
usecache=0
sref=1
sbid=0
shopbutton2=0
shopscroll=0
bgs=pygame.Surface((0,0))
downloadqueue=[]
search=''
progress=0
srank=1
maxsentry=10
loading=Tween(begin=0, end=1,duration=1000,easing=Easing.BOUNCE,easing_mode=EasingMode.OUT,boomerang=True,loop=True)
loading.start()
def reload_background(value):
    global bgs
    bgs=pygame.Surface((0,0))
    try:
        bgst=requests.get("https://assets.ppy.sh/beatmaps/"+str(value)+'/covers/card.jpg?0',headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=3)
        bgst=bgst.content
        bgst=io.BytesIO(bgst)
        bgst=pygame.image.load(bgst).convert()
        bgs=pygame.transform.smoothscale(bgst, (350,180))
    except Exception:
        pass
def getrank(id):
    if id==3 or id==4:
        return 2
    if id==-1:
        return 2
    elif id>0:
        return 0
    else:
        return 1
def shop_refresh(usecached):
    global sbt,sentrynf,sref,serr,sentry,progress
    serr=0
    try:
        if not usecached:
            sref=1
            if search!='':
                alt='?query='+str(search)
            else:
                alt=''
            sentrynf=[]
            tick=0
            retry=1
            while retry:
                try:
                    f = requests.get(beatmapapi+'search'+alt+'?limit=50',headers={'User-Agent': 'QluteClient'},timeout=10)
                    sentrynf=json.loads(f.text)
                    retry=0
                except Exception as err:
                    print(err,'shopref')
        sentry=[]
        tmp=[]
        for a in sentrynf:
            if getrank(a['RankedStatus'])==srank:
                sentry.append(a)
                tmp.append((a['Artist'],a['Title']))
        sbt=tmp
        sref=0
    except Exception as err:
        print(err,'> Store')
        serr=1
def downloads(screen,w,h):
    global sysbutton,dq,dqs,serr,shopscroll
    if getactivity()==8:
        dq=[]
        dqu=[]
        dqh=''
        for a in getqueue():
            if str(a[2])!='Queued':
                dqh='%'
            dqu.append(str(a[2])+dqh+' - '+str(a[0]))
        pygame.draw.rect(screen,maincolour[0],(0,100,w,h-160))
        for a in range(1,len(getqueue())+1):
            dq.append(((w//2)-200,shopscroll+100+(80*(a-1)),400,80))
        dqs=draw_button(screen,dq,dqu,border_radius=0,selected_button=sbid)
        pygame.draw.rect(screen,maincolour[2],(0,0,w,100))
        pygame.draw.rect(screen,maincolour[2],(0,h-60,w,60))
        screen.blit(getfonts(2).render('Downloads',True,(255,255,255)),(20,20))
        sysbutton=draw_button(screen,((0,h-60,100,60),),('Back',),border_radius=0)
        for event in get_input():
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if sysbutton:
                    transitionprep(1)
                elif event.button==4:
                    if not shopscroll+40>0:
                        shopscroll+=40
                elif event.button==5:
                    if not shopscroll-40<-(80*(len(dq)-1)):
                        shopscroll-=40

def shopdirect(screen,w,h):
    global shopref,sysbutton,shopbutton,serr,shopbutton2,usecache,shopscroll,sbid,sbt,srank,search
    if getactivity()==4:
        if shopref or serr:
            threading.Thread(target=shop_refresh, args=(usecache,)).start()
            shopref=0
            usecache=0
            serr=0
        pygame.draw.rect(screen,maincolour[1],(0,100,w,h-160))
        obj=0
        id=0
        mouse=pygame.mouse.get_pos()
        buttonid=0
        click=0
        for a in sbt:
            offset=shopscroll+(80*id)+120
            if 0>=-offset and -offset>=-h+80:
                scr=pygame.surface.Surface((w-400,80))
                if pygame.Rect.collidepoint(pygame.Rect(0,offset,w//2,80),mouse[0],mouse[1]):
                    hover=20
                    buttonid=id
                    click=1
                else:
                    hover=0
                if id==sbid-1:
                    scr.fill(maincolour[3])
                else:
                    scr.fill((maincolour[2][0]+hover,maincolour[2][1]+hover,maincolour[2][2]+hover))
                meta = getfonts(0).render(a[0],True,(255,255,255)), getfonts(0).render(a[1],True,(255,255,255))
                scr.blit(meta[0],(15,10))
                scr.blit(meta[1],(15,50))
                screen.blit(scr,(0,offset))
                obj+=1
            id+=1
        pygame.draw.rect(screen,maincolour[8],(w-400,100,400,h-160))
        pygame.draw.rect(screen,maincolour[2],(0,h-60,w,60))
        pygame.draw.rect(screen,maincolour[2],(0,100,w-400,20))
        pygame.draw.rect(screen,maincolour[2],(0,0,w,100))
        screen.blit(getfonts(2).render('Browse',True,(255,255,255)),(20,20))
        shopbutton2=draw_button(screen,((0,100,100,20),(300,80,100,20),(100,100,100,20),(200,100,100,20),(300,100,100,20),), ('Refresh','Search','Ranked','Unranked','Special'),fonttype=1,border_radius=0,selected_button=srank+3)
        textbox(screen,(0,80,300),20,text=search,center=True,min=True,bg_colour=maincolour[8])

        
        if sref:
            loading.update()
            pygame.draw.rect(screen,(255,255,255),(25+(loading.value*(w-485)),h//2-25,40,40),border_radius=int(40-(loading.value*25)))
            pygame.draw.rect(screen,(0,0,0),(27+(loading.value*(w-485)),h//2-22,35,35),border_radius=int(35-(loading.value*25)))
            te='Loading...'
            center_text(screen,te,(400*((w/800)-1),120,400,h-100),type='grade')
        if len(sbt):
            scrollbar(screen,(0,120),(10,h-180),search=shopscroll//80,length=len(sbt))
        if sbid:
            crok=0
            entry=sentry[sbid-1]
            rank=getrank(entry['RankedStatus'])
            pygame.draw.rect(screen,(50,50,50),(w-400+25,120,350,180))
            screen.blit(bgs,(w-400+25,120))
            screen.blit(getfonts(0).render(entry['Title'],True,(255,255,255)),(w-400+25,340))
            screen.blit(getfonts(0).render(entry['Artist'],True,(255,255,255)),(w-400+25,370))
            screen.blit(getfonts(0).render(entry['Creator'],True,(255,255,255)),(w-400+25,400))
            if entry['ChildrenBeatmaps'][0]['MaxCombo']:
                com=entry['ChildrenBeatmaps'][0]['MaxCombo']
            else:
                com=0
            screen.blit(getfonts(0).render(str('BPM:'+str(entry['ChildrenBeatmaps'][0]['BPM'])+' - '+str(getpoint(com,0,0,0,1,combo=com))+'pp - '+clockify(entry['ChildrenBeatmaps'][0]['TotalLength']*1000)),True,(255,255,255)),(w-400+25,310))
            pygame.draw.rect(screen,rankmodes[rank][1],(w-400+25,260,100,40),border_top_right_radius=10)
            center_text(screen,rankmodes[rank][0],(w-400+25,265,100,35  ))
        else:
            crok=999

        sysbutton=draw_button(screen,((-10,h-60,100,60),(w-140,crok+h-60,140,60)),('Back','Download'),border_radius=0)

        ## Input
        for event in get_input():
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if sysbutton==1:
                    transitionprep(1)
                elif sysbutton==2:
                    notification('Downloading',desc=sentry[sbid-1]['Artist']+' - '+str(sentry[sbid-1]['Title']))
                    downloadmap(mainurl+'/d/'+str(sentry[sbid-1]['ChildrenBeatmaps'][0]['ParentSetID']),str(sentry[sbid-1]['Title']+' - '+sentry[sbid-1]['Artist']))
                elif event.button==1:
                    if shopbutton2 in (1,2):
                       if not sref:
                            shopref=1
                            sb=[]
                            sbt=[]
                    elif shopbutton2>2:
                        if srank!=shopbutton2-3:
                            if not sref:
                                srank=shopbutton2-3
                                usecache=1
                                sbid=0
                                shopref=1
                                shopscroll=0
                    elif buttonid+1 != sbid and click:
                        sbid=buttonid+1
                        threading.Thread(target=reload_background, args=(sentry[sbid-1]['SetID'],)).start()
                    elif buttonid+1 == sbid and click:
                        notification('Downloading',desc=sentry[sbid-1]['Artist']+' - '+str(sentry[sbid-1]['Title']))
                        downloadmap(mainurl+'/d/'+str(sentry[sbid-1]['ChildrenBeatmaps'][0]['ParentSetID']),str(sentry[sbid-1]['Title']+' - '+sentry[sbid-1]['Artist']))
                elif event.button==4:
                    if not shopscroll+40>0:
                        shopscroll+=40
                elif event.button==5:
                    if not shopscroll-40<-(80*(len(sbt)-1)):
                        shopscroll-=40
            elif event.type == pygame.KEYDOWN:
                if event.key  ==  pygame.K_RETURN:
                    shopref=1
                    sb=[]
                    sbt=[]
                elif event.key == pygame.K_BACKSPACE: 
                    search = search[:-1]
                else:
                    search += event.unicode
