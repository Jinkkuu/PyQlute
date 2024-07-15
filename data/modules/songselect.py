import pygame.gfxdraw,time,threading,os
import data.modules.renderapi as renderapi
from data.modules.bootstrap import getactivity,setactivity,transitionprep,gamepath,sify,clockify,scrollbar,getact,getimg,setmsg,timeform,getuserdata
from data.modules.beatmap_processor import get_info,cache_beatmap,grabobjects,getobjects,random_beatmap,reloadbg,getbackground,loadstats,beatmaplist,beatmapselect,getkeycount
from data.modules.colours import maincolour,emblemcolour
from data.modules.audio import load_music,music_control,set_gametime
from data.modules.input import get_input
from data.modules.gameplay import resetcursor,reset_score
from data.modules.card import main as card
from data.modules.shopscreen import rankmodes
from data.modules.onlineapi import getmystats,getleaderboard,rleaderboard,getstat
from data.modules.settings import getsetting
import pygame
from tweener import *
cross=[0,0,0]
selected=[0,0]
diffsec=0
songani=[[Tween(),0],[Tween(),0]]
modsen=[0,0,0,0,0,0,0,0,0,0]
modshow=0
modsv=0
modsani=[Tween(begin=0, end=1,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
modsani[0].start()
modsalias="Auto",'Blind','Slice','EZ','Random','Strict'#,'DT','HT'
modsaliasab='AT','BD','SL','EZ','RND','SN'#,'DT','HT'
mods=''
starrating=0 # Star Rating
if os.path.isfile(getuserdata()+'.developer'):
    modsen[0]=1 # Automatically enables Auto Mod
def getmult():
    scoremult=1
    for a in range(2,len(modsen)+1):
        if modsen[a-1] and a==2:
            scoremult+=1.5
        elif modsen[a-1] and a == 6:
            scoremult+=0.8
        elif modsen[a-1] and not a in (4,5,7,8):
            scoremult+=0.5
        elif modsen[a-1] and (a in (4,7)):
            scoremult/=2
    return scoremult
def get_mods(screen,bpos):
    global mods
    b=0
    tap=0
    mods=''
    img=getimg('emblem.png')
    for a in modsaliasab:
        if modsen[b]:
            pos=(bpos[0]+(15*tap),bpos[1])
            rec=img.get_rect() 
            screen.blit(getimg('emblem.png'),pos) 
            mods+=a
            renderapi.center_text(screen,a,(pos[0],pos[1]+2,rec[2],rec[3]),'',(emblemcolour))
            tap+=1
        b+=1
def ecross(id,val):
    global cross
    cross[id]=val
def resetdcursor():
    global cross,selected
    cross[1] = 0
    selected[1] = 0
def startani(val):
    global songani
    songani[val]=[Tween(begin=cross[val], end=-selected[val]*80,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
    songani[val][0].start()
olds=0,0
def main(screen,w,h):
    global cross,selected,diffsec,modshow,modsani,modsv,modsen,lpanel,panel,olds
    from data.modules.mainmenu import flashscr
    from data.modules.onlineapi import ranktype
    if not "lpanel" in globals():
        lpanel=pygame.surface.Surface((280,320),pygame.SRCALPHA, 32).convert_alpha()
        lpanel.set_alpha(216)
    else:
        lpanel.fill((0,0,0,0))
    if getactivity() == 2:
        from data.modules.beatmap_processor import beatmaplist,beatmapselect
        if olds!=(w,h):
            olds=w,h
            panel=pygame.surface.Surface((300,olds[1]-120))
            panel.set_alpha(51)
            panel.fill(0)
        parallax=((pygame.mouse.get_pos()[0]/w)*10)-5,((pygame.mouse.get_pos()[1]/h)*10)-5
        mult=getmult()
        modsani[0].update()
        if modsani[0].value==100 or not modshow:
            modsani[1]=0
        if songani[diffsec][0].value==-selected[diffsec]*80:
            songani[diffsec][1]=1
        elif not songani[diffsec][1]:
            songani[diffsec][0].update()
            cross[diffsec]=songani[diffsec][0].value
        obj=0
        leadmode=0
        tm=[]
        mouse=pygame.mouse.get_pos()
        buttonid=0
        click=0
        bg=getbackground(w,h)
        if bg:
            screen.blit(bg,(-5-parallax[0],-5-parallax[1]))
        else:
            screen.fill((maincolour[4]))
        screen.blit(flashscr,(0,0))
        screen.blit(panel,(0,60))
        #pygame.draw.rect(screen,(255,255,255,51),)
        #pygame.Surface.blits(screen,((panel,(0,60))))
        
        #panelf=pygame.surface.Surface((200,h-60))
        if mult!=1:
            modtext=str(round(mult,2))+'x'
        else:
            modtext='Mods'
        beatcount=len(beatmapselect)
        diffs=get_info('maps')
        pos=int(-cross[diffsec]//40//2)
        if pos-10>0:
            pos-=10
        else:
            pos=0
        end=pos+20
        id=pos
        oid=0
        if beatcount:
            i=(beatmapselect,diffs)
            for a in i[diffsec][pos:end]:
                offset=cross[diffsec]+(80*id)+(h//2-80)
                if 0>=-offset and -offset>=-h+60:
                    if pygame.Rect.collidepoint(pygame.Rect(w//2,offset,w//2,80),mouse[0],mouse[1]):
                        hover=20
                        buttonid=id
                        click=1
                        col=(maincolour[2][0]+hover,maincolour[2][1]+hover,maincolour[2][2]+hover)
                    else:
                        hover=0
                        if id==selected[diffsec]:
                            col = maincolour[3]
                        else:
                            col=maincolour[2]
                    if getsetting('classicmode'):
                        scr=pygame.surface.Surface((w//2,80),pygame.SRCALPHA)
                        scr.fill((0,0,0,0))
                        pygame.draw.rect(scr,col,(0,3,w//2+10,75),border_radius=10)
                    else:
                        scr=pygame.surface.Surface((w//2,80))
                        scr.fill(col)
                    if not diffsec:
                        meta = renderapi.getfonts(0).render(a['title'],True,(255,255,255)), renderapi.getfonts(0).render(a['artist']+' (mapped by '+str(a['creator'])+')',True,(255,255,255))
                    else:
                        meta = renderapi.getfonts(0).render(a,True,(255,255,255)),renderapi.getfonts(0).render(str(int(get_info('points')[id]*mult))+'pp',True,(255,255,255))
                    scr.blit(meta[0],(10,10))
                    scr.blit(meta[1],(10,50))
                    scr.set_alpha(255*0.95)
                    screen.blit(scr,(w//2,offset))
                    obj+=1
                id+=1
                oid+=1

            points=get_info('points')
            pp=(int(points[0]),int(points[-1]))
            sifyy=sify(len(diffs),' Set')
            tmp = renderapi.getfonts(0).render(str(len(diffs))+sifyy+' - '+clockify(get_info('lengths')[selected[1]]),True,(255,255,255))
            screen.blit(tmp,(20,80))
            t=renderapi.getfonts(0).render(rankmodes[ranktype][0],True,(255,255,255))
            rtl=t.get_rect()
            fr=rtl
            rtl=290-rtl[2],80
            pygame.draw.rect(screen,rankmodes[ranktype][1],(rtl[0],rtl[1],fr[2]+10,35),border_bottom_left_radius=10,border_top_left_radius=10)
            screen.blit(t,(rtl[0]+5,rtl[1]+7))
            t=renderapi.getfonts(0).render(str(round(starrating*(mult+1)/2,2))+' Stars',True,(255,255,255))
            rtl=t.get_rect()
            fr=rtl
            rtl=290-rtl[2],125
            screen.blit(t,(rtl[0],rtl[1]))
            if pp[0] != pp[1]:
                tmp = renderapi.getfonts(0).render(format(int(pp[0]*mult),',')+'-'+format(int(pp[1]*mult),',')+'pp',True,(255,255,255))
            else:
                tmp = renderapi.getfonts(0).render(format(int(pp[0]*mult),',')+'pp',True,(255,255,255))
            if len(diffs)>1 and not diffsec:
                starticon='next.png'
            else:
                starticon='go.png'
            screen.blit(tmp,(20,125))
            scrollbar(screen,(w-10,60),(10,h-140),search=cross[diffsec]/80,length=len(i[diffsec]))
        
        if getsetting('leaderboard'): 
            c=0
            lead=getleaderboard()
            if len(lead):
                for a in lead: 
                    if a['username']==getsetting('username'): 
                        col=166, 207, 255
                    else:
                        col=(255,255,255) 
                    leadpos=(0,60*c+cross[2],300,60)
                    if pygame.Rect.collidepoint(pygame.Rect(leadpos[0]+10,leadpos[1]+h//2-140,leadpos[2],leadpos[3]),mouse[0],mouse[1]):
                        hov=20
                        leadmode=1
                    else:
                        hov=0
                    pygame.draw.rect(lpanel,(maincolour[0][0]+hov,maincolour[0][1]+hov,maincolour[0][2]+hov),pygame.Rect(leadpos)) 
                    lpanel.blit(renderapi.getfonts(0).render('#'+str(c+1)+' '+a["username"],True,col),(leadpos[0]+10,leadpos[1]+10))
                    lpanel.blit(renderapi.getfonts(1).render(format(int(a['score']),',')+' - '+str(int(a["points"]))+'pp ('+str(int(a['combo']))+'x) '+timeform(int(time.time()-a['time'])),True,(255,255,255)),(leadpos[0]+10,leadpos[1]+38))
                    renderapi.center_text(lpanel,a['mods'],(leadpos[0]+250,leadpos[1]+45,0,0),('rtl','min'),(255,255,255)) 
                    c+=1
                if c>5:
                    scrollbar(lpanel,(0,0),(10,300),search=cross[2]/60,length=len(lead)*60,colour=(255,255,255))
            else:
                renderapi.center_text(lpanel,'No Scores set ;-;',lpanel.get_rect(),'')
            screen.blit(lpanel,(10,h//2-140))
        if modsani[1]: # Animation for Mod Select :3
            pop=modsani[0].value
        else:
            pop=1-modsani[0].value
        if not modsani[1]:
            mod=0
        get_mods(screen,(100,h-(110*(1-pop))))
        pygame.draw.rect(screen,maincolour[0],pygame.Rect(0,h-(170*pop),430,120),border_top_left_radius=10,border_top_right_radius=10)
        #(340,h-160,90,40) ~ Placeholder
        # This will be here for now, it WILL get better and more optimized over time
        t=(20,20,120,120,220,320,420,480)
        tm=[]
        for b in range(1,len(t)+1): # Ewwwwwww
            if (b == 2 and modsen[2]) or (b == 3 and modsen[1]):
                tm.append(-999)
            else:
                tm.append(t[b-1])
        mod,modh=renderapi.draw_button(screen,((tm[0],h-(160*pop),90,40) ,(tm[1],h-(110*pop),90,40) ,(tm[2],h-(160*pop),90,40) ,(tm[3],h-(110*pop),90,40) ,(tm[4],h-(160*pop),90,40) ,(tm[5],h-(160*pop),90,40)),modsalias,return_hover=1,enabled_button=modsen)
        pygame.draw.rect(screen,maincolour[1],pygame.Rect(0,h-60,w,60))
        card(screen,(w//2-80,h-55),mini=1,accuracy=getmystats()[0],points=getmystats()[1],rank=getmystats()[2],username=getsetting('username'))
        
        
        if  beatcount:
            title = get_info('songtitle')
            gobutton = renderapi.draw_button(screen,((w-120,h-80,130,90),),('',),border_radius=10,icon=(starticon,),hidetext=1)
        else:
            gobutton = 0
            title = 'No Beatmaps Installed :<'
        pygame.draw.rect(screen,maincolour[1],pygame.Rect(0,0,w,60))
        
        button = renderapi.draw_button(screen,((0,h-60,100,60),(100,h-60,100,60),),('Back',modtext),border_radius=0)
        tmp = renderapi.getfonts(0).render(title,True,(255,255,255))
        screen.blit(tmp,(20,20))
        #screen.blit(renderapi.getfonts(1).render(str(obj)+' out of '+str((id,oid))+' Objects ('+str(pos)+' pos)',True,(255,255,255)),(10,10))
        

# MSG tooltip
        if modh==0:
            setmsg('View a perfect play (0)')
        elif modh==1:
            setmsg("Beat to the rhythm (+1.5)")
        elif modh==2:
            setmsg('Half blind (+0.5)')
        elif modh==3:
            setmsg("makes everything easy (/0.5)")
        elif modh==4:
            setmsg('Adds new fun! (0)')
        elif modh==5:
            setmsg('You have to aim your hits right! (+0.8)')
        elif modh==6:
            setmsg('We be easy on you (/0.5)')





        for event in get_input():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button == 1:
                        if diffsec:
                            diffsec = not diffsec
                        else:
                            transitionprep(1)
                    elif button == 2:
                        modshow = not modshow
                        modsani=[Tween(begin=modsv, end=1,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),modshow]
                        modsv=modsani[0].value
                        modsani[0].start()
                    elif mod:
                        modsen[mod-1]=not modsen[mod-1]
                    elif gobutton:
                        if not diffsec and len(diffs)>1:
                            diffsec = not diffsec
                        else:
                            transitionprep(5)
                            reload_map()
                    elif buttonid != selected[diffsec] and click:
                        prepare(buttonid,reloadmusic=not diffsec,getranky=not diffsec)
                    elif buttonid == selected[diffsec] and click:
                        if not diffsec and len(diffs)>1:
                            diffsec = not diffsec
                        else:
                            transitionprep(5)
                            reload_map()
                if event.button == 4:
                    if cross[diffsec]<0 and not leadmode:
                        cross[diffsec]+=40
                    elif cross[2]<0 and leadmode:
                        cross[2]+=30
                elif event.button == 5:
                    if cross[diffsec]-40>(80*-id)+40 and not leadmode:
                        cross[diffsec]-=40
                    elif cross[2]-60>(60*-len(lead))+(4*60) and leadmode:
                        cross[2]-=30
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END and len(beatmaplist):
                    i=(beatmapselect,diffs)
                    selected[diffsec]=len(i[diffsec])-1
                    prepare(selected[diffsec],reloadmusic=not diffsec,getranky=not diffsec)
                    resetdcursor()
                elif event.key in (pygame.K_ESCAPE,pygame.K_q):
                    if diffsec:
                        diffsec=not diffsec
                    else:
                        transitionprep(1)
                elif event.key == pygame.K_RETURN and len(beatmaplist):
                    if not diffsec and len(diffs)>1:
                        diffsec = not diffsec
                    else:
                        transitionprep(5)
                        reload_map()
                elif event.key == pygame.K_UP and len(beatmaplist):
                    if selected[diffsec]>0:
                        selected[diffsec]-=1
                    else:
                        selected[diffsec] = id-1
                    prepare(selected[diffsec],reloadmusic=not diffsec,getranky=not diffsec)
                    if not diffsec:
                        resetdcursor()                    
                elif event.key == pygame.K_F1:
                    modshow = not modshow
                    modsani=[Tween(begin=modsv, end=1,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),modshow]
                    modsv=modsani[0].value
                    modsani[0].start()
                elif event.key == pygame.K_F2 and len(beatmaplist) and not diffsec:
                    tmp=random_beatmap()
                    prepare(list(beatmaplist.keys()).index(tmp['songtitle']),reloadmusic=not diffsec,getranky=not diffsec)
                    resetdcursor()                    
                elif event.key == pygame.K_DOWN and len(beatmaplist):
                    if not selected[diffsec] >= id-1:
                        selected[diffsec]+=1
                    else:
                        selected[diffsec]=0
                    prepare(selected[diffsec],reloadmusic=not diffsec,getranky=not diffsec)
                    if not diffsec:
                        resetdcursor()                    

                elif event.key == pygame.K_HOME and len(beatmaplist):
                    selected[diffsec]=0
                    prepare(selected[diffsec])
                    resetdcursor()     
def getmaxpoints():
    p=get_info('points')[selected[1]]*getmult()
    return p               
def reload_map():
    from data.modules.beatmap_processor import beatmapselect
    if len(beatmaplist):
        selectedqueue = beatmapselect[selected[0]]['songtitle'],beatmapselect[selected[0]]['raw'],beatmapselect[selected[0]]['audiofile']
        if getact() != 5:
            startani(diffsec)
            if selectedqueue[2]:
                load_music(gamepath+selectedqueue[1]+'/'+selectedqueue[2])
        else:
            set_gametime(5)
            music_control(1)
            reset_score()
            resetcursor()
            cache_beatmap(selectedqueue[0])
def prepare(buttonid,reloadmusic=True,reloadleaderboard=True,getranky=False):
    global selected,starrating
    from data.modules.beatmap_processor import beatmapselect
    reset_score()
    selected[diffsec]=buttonid
    if not diffsec:
        selected[1]=0
        cross[1]=0
    selid=0
    if get_info('maps'):
        if selected[1]<=len(get_info('maps')):
            selid=selected[1]
        diff=get_info('maps')[selid]
        acc=1
    else:
        acc=0
    selectedqueue = beatmapselect[selected[0]]['songtitle'],beatmapselect[selected[0]]['raw'],beatmapselect[selected[0]]['audiofile'],beatmapselect[selected[0]]['diffurl'][selid]
    cache_beatmap(selectedqueue[0])
    resetcursor()
    mod=selectedqueue[0].replace(' [no video]','')
    reloadbg(gamepath+selectedqueue[1]+'/'+selectedqueue[3],gamepath+selectedqueue[1]+'/')
    if reloadleaderboard:
        threading.Thread(target=rleaderboard, args=(get_info('beatmapids')[selected[1]],)).start()
    if getranky:
        threading.Thread(target=getstat, args=(get_info('beatmapsetid'),)).start()
    if mod[0]==' ':
        mod=mod[1:]
    creator=get_info('creator')
    starrating=0
    if acc:
        grabobjects(gamepath+selectedqueue[1]+'/'+get_info('diffurl')[selid])
        bpm=get_info('bpm')
        x=0
        for a in getobjects():
            so=int(a[2])
            if so>x:
                suna=((so-x)/bpm)
                if not suna<1.1:
                    suna=0
                #print('[S U N A]',round(suna,2),str(round(starrating,2))+' Stars ')
                starrating+=suna*0.01
                x=so
    else:
        print('No maps found')
    startani(diffsec)
    if selectedqueue[2] and reloadmusic:
        load_music(gamepath+selectedqueue[1]+'/'+selectedqueue[2],-1,fadein=1)
oh=0
ow=0