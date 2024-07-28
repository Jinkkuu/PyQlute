import pygame.gfxdraw,time,threading,os
import data.modules.renderapi as renderapi
from data.modules.bootstrap import getactivity,setactivity,transitionprep,gamepath,sify,clockify,scrollbar,getact,getimg,setmsg,timeform,getuserdata
from data.modules.beatmap_processor import get_info,cache_beatmap,grabobjects,getobjects,random_beatmap,reloadbg,getbackground,loadstats,beatmaplist,getkeycount,suna
from data.modules.colours import maincolour,emblemcolour,songselectcolour,mapidlecolour,mapselectedcolour
from data.modules.audio import load_music,music_control,set_gametime
from data.modules.input import get_input
from data.modules.gameplay import resetcursor,reset_score,getpoint
from data.modules.card import main as card
from data.modules.shopscreen import rankmodes
from data.modules.onlineapi import getmystats,getleaderboard,rleaderboard,getstat,getlocalleaderboard,rlocalleaderboard
from data.modules.settings import getsetting,setsetting
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
modsalias="Auto",'Blind','Slice','EZ','Strict'#,'DT','HT'
modsaliasab='AT','BD','SL','EZ','SN'#,'DT','HT'
mods=''
altbutton=0
starrating=0 # Star Rating
if os.path.isfile(getuserdata()+'.developer'):
    modsen[0]=1 # Automatically enables Auto Mod
def getmult():
    scoremult=1
    for a in range(2,len(modsen)+1):
        if modsen[a-1] and a==2:
            scoremult+=1.5
        elif modsen[a-1] and a == 5:
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
    global cross,selected,diffsec,modshow,modsani,modsv,modsen,lpanel,panel,olds,altbutton
    from data.modules.mainmenu import getflash
    from data.modules.onlineapi import ranktype
    if not "lpanel" in globals():
        lpanel=pygame.surface.Surface((280,320),pygame.SRCALPHA, 32).convert_alpha()
    else:
        lpanel.fill((0,0,0,0))
    if getactivity() == 2:
        from data.modules.beatmap_processor import beatmaplist
        if olds!=(w,h):
            olds=w,h
            panel=pygame.surface.Surface((w,h),pygame.SRCALPHA, 32).convert_alpha()
            pygame.draw.polygon(panel,(0,0,0),((w,h),(0,h),(0,0),(w,0),(w,60),(300,60),(300,h-60),(w,h-60)))
            panel.set_alpha(100)
        mouse=pygame.mouse.get_pos()
        parallax=((mouse[0]/w)*10)-5,((mouse[1]/h)*10)-5
        parallax=(-5-parallax[0],-5-parallax[1])
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
        buttonid=0
        click=0
        bg=getbackground(w,h)
        screen.fill((maincolour[4]))
        if bg and len(beatmaplist):
            bgrect=bg.get_rect(center = screen.get_rect().center)[:2]
            screen.blit(bg,(bgrect[0]-parallax[0],bgrect[1]-parallax[1]))
        screen.blit(getflash(),(0,0))
        if mult!=1:
            modtext=str(round(mult,2))+'x'
        else:
            modtext='Mods'
        beatcount=len(beatmaplist)
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
            i=(beatmaplist,eval(diffs))
            for a in i[diffsec][pos:end]:
                offset=cross[diffsec]+(80*id)+(h//2-80)
                if 0>=-offset-60 and -offset>=-h:
                    if pygame.Rect.collidepoint(pygame.Rect(w//2,offset,w//2,80),mouse[0],mouse[1]):
                        hover=20
                        buttonid=id
                        click=1
                        if id==selected[diffsec]:
                            col = mapselectedcolour
                        else:
                            col=(mapidlecolour[0]+hover,mapidlecolour[1]+hover,mapidlecolour[2]+hover)
                    else:
                        hover=0
                        if id==selected[diffsec]:
                            col = mapselectedcolour
                        else:
                            col=mapidlecolour
                    scr=pygame.surface.Surface((w//2,80))
                    scr.fill(col)
                    if not diffsec:
                        meta = renderapi.getfonts(0).render(a['title'],True,(255,255,255)), renderapi.getfonts(0).render(str(a['artist'])+' (mapped by '+str(a['creator'])+')',True,(255,255,255))
                        scr.blit(meta[0],(10,10))
                        scr.blit(meta[1],(10,50))
                    else:
                        meta = renderapi.getfonts(0).render(a,True,(255,255,255))#,renderapi.getfonts(0).render(str()+' Stars',True,(255,255,255))
                        scr.blit(meta,(10,10))
                        star=round(eval(get_info('starratings'))[id]*(mult+1)/2,2)
                        if star>10.99:
                            star=10.99
                        pygame.draw.rect(scr,(50,50,50),(10,50,300,10))
                        pygame.draw.rect(scr,(255,255,255),(10,50,(star/10.99)*300,10))
                    #scr.blit(meta[1],(10,50))
                    screen.blit(scr,(w//2,offset))
                    obj+=1
                id+=1
                oid+=1
            if len(diffs)>1 and not diffsec:
                starticon='next.png'
            else:
                starticon='go.png'
            scrollbar(screen,(w-10,60),(10,h-140),search=cross[diffsec]/80,length=len(i[diffsec]))
        screen.blit(panel,(0,0))
        if beatcount:
            t=renderapi.getfonts(0).render(rankmodes[ranktype][0],True,(255,255,255))
            rtl=t.get_rect()
            fr=rtl
            rtl=290-rtl[2],65
            screen.blit(renderapi.getfonts(0).render(str(60000//get_info('bpm'))+' BPM',True,(255,255,255)),(10,rtl[1]+7))
            pygame.draw.rect(screen,rankmodes[ranktype][1],(rtl[0],rtl[1],fr[2]+10,35),border_bottom_left_radius=10,border_top_left_radius=10)
            screen.blit(t,(rtl[0]+5,rtl[1]+7))
            t=renderapi.getfonts(0).render(str(round(starrating*(mult+1)/2,2))+' Stars',True,(255,255,255))
            rtl=t.get_rect()
            fr=rtl
            rtl=290-rtl[2],110
            screen.blit(t,(rtl[0],rtl[1]))
            if altbutton:
                tmp = renderapi.getfonts(0).render(str(getmaxpoints())+'pp',True,(255,255,255))
            else:
                tmp = renderapi.getfonts(0).render(clockify(eval(get_info('lengths'))[selected[1]]),True,(255,255,255))
            screen.blit(tmp,(10,110))
        
        if getsetting('leaderboard'): 
            leadbutton=renderapi.draw_button(screen,((10,h//2-160,140,20),(150,h//2-160,140,20)), ('Local','Online'),fonttype=1,border_radius=0,selected_button=getsetting('leaderboardtype')+1)
            if leadbutton:
                setsetting('leaderboardtype',leadbutton-1)
                if getsetting('leaderboardtype'): 
                    threading.Thread(target=rleaderboard, args=(eval(get_info('beatmapids'))[selected[1]],)).start()
                else:
                    rlocalleaderboard(eval(get_info('beatmapids'))[selected[1]])
            c=0
            if getsetting('leaderboardtype'): 
                lead=getleaderboard()
            else:
                lead=getlocalleaderboard()
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
                    pygame.draw.rect(lpanel,(mapidlecolour[0]+hov,mapidlecolour[1]+hov,mapidlecolour[2]+hov),pygame.Rect(leadpos)) 
                    lpanel.blit(renderapi.getfonts(0).render('#'+str(c+1)+' '+a["username"],True,col),(leadpos[0]+10,leadpos[1]+10))
                    lpanel.blit(renderapi.getfonts(1).render(format(int(a['score']),',')+' - '+str(int(a["points"]))+'pp ('+str(int(a['combo']))+'x) '+timeform(int(time.time()-a['time'])),True,(255,255,255)),(leadpos[0]+10,leadpos[1]+38))
                    t=renderapi.getfonts(1).render(a['mods'],True,(255,255,255))
                    rtl=t.get_rect()
                    fr=rtl
                    rtl=270-fr[2],leadpos[1]+38
                    lpanel.blit(t,rtl)
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
        pygame.draw.rect(screen,maincolour[0],pygame.Rect((380*pop)-420,h-170,380,110),border_top_right_radius=10,border_bottom_right_radius=10)
        #(340,h-160,90,40) ~ Placeholder
        # This will be here for now, it WILL get better and more optimized over time
        t=(20,20,120,120,220,320,420,480)
        tm=[]
        for b in range(1,len(t)+1): # Ewwwwwww
            if (b == 2 and modsen[2]) or (b == 3 and modsen[1]):
                tm.append(-999)
            else:
                tm.append(t[b-1])
        mod,modh=renderapi.draw_button(screen,((tm[0]+(100*pop)-110,h-160,90,40) ,(tm[1]+(100*pop)-110,h-110,90,40) ,(tm[2]+(200*pop)-210,h-160,90,40) ,(tm[3]+(200*pop)-210,h-110,90,40) ,(tm[4]+(300*pop)-310,h-160,90,40)),modsalias,return_hover=1,enabled_button=modsen)
        pygame.draw.rect(screen,songselectcolour,(w//2-80,h-60,300,60))
        card(screen,(w//2-80,h-55),hidebg=1,overidecolour=(100,100,100),mini=1,accuracy=getmystats()[0],points=getmystats()[1],rank=getmystats()[2],username=getsetting('username'))
        
        
        if  beatcount:
            title = get_info('songtitle')
            gobutton = renderapi.draw_button(screen,((w-120,h-80,130,90),),('',),border_radius=10,icon=(starticon,),hidetext=1)
        else:
            gobutton = 0
            title = 'No Beatmaps Installed :<'
        button = button = renderapi.draw_button(screen,((0,h-60,100,60),(100,h-60,100,60),(200,h,100,60),),('Back',modtext,'Quest'),border_radius=0)
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
            setmsg('You have to aim your hits right! (+0.8)')
        elif modh==5:
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
                        reloadpoints()
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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LALT:
                    altbutton=0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END and len(beatmaplist):
                    i=(beatmaplist,eval(diffs))
                    selected[diffsec]=len(i[diffsec])-1
                    prepare(selected[diffsec],reloadmusic=not diffsec,getranky=not diffsec)
                    resetdcursor()
                elif event.key in (pygame.K_ESCAPE,pygame.K_q):
                    if diffsec:
                        diffsec=not diffsec
                    else:
                        transitionprep(1)
                elif event.key == pygame.K_LALT:
                    altbutton=1
                elif event.key == pygame.K_RETURN and len(beatmaplist):
                    if not diffsec and len(eval(diffs))>1:
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
                    prepare(tmp[1],reloadmusic=not diffsec,getranky=not diffsec)
                    resetdcursor()                    
                elif event.key == pygame.K_DOWN and len(beatmaplist):
                    if not selected[diffsec] >= id-1:
                        selected[diffsec]+=1
                    else:
                        selected[diffsec]=0
                    prepare(selected[diffsec],reloadmusic=not diffsec,getranky=not diffsec)
                    if not diffsec:
                        resetdcursor()                    

                elif event.key == pygame.K_HOME and len(beatmaplist) and not diffsec:
                    selected[diffsec]=0
                    prepare(selected[diffsec])
                    resetdcursor()       
def reload_map():
    global maxpoints
    from data.modules.beatmap_processor import beatmaplist
    from data.modules.songselect import selected
    if len(beatmaplist):
        selectedqueue = beatmaplist[selected[0]]['songtitle'],beatmaplist[selected[0]]['raw'],beatmaplist[selected[0]]['audiofile']
        if getact() != 5:
            startani(diffsec)
            if selectedqueue[2]:
                load_music(gamepath+selectedqueue[1]+'/'+selectedqueue[2])
        else:
            set_gametime(5)
            music_control(1)
            reset_score()
            resetcursor()
            cache_beatmap(selected[0])
def getmaxpoints():
    return maxpoints      
def reloadpoints():
    global maxpoints
    maxpoints = int(getpoint(len(getobjects()),0,0,0,1,len(getobjects()),int)*getmult())
def prepare(buttonid,reloadmusic=True,reloadleaderboard=True,getranky=False):
    global selected,starrating,maxpoints
    from data.modules.beatmap_processor import beatmaplist
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
    selectedqueue = beatmaplist[selected[0]]['songtitle'],beatmaplist[selected[0]]['raw'],beatmaplist[selected[0]]['audiofile'],eval(beatmaplist[selected[0]]['diffurl'])[selid]
    cache_beatmap(selected[0])
    resetcursor()
    mod=selectedqueue[0].replace(' [no video]','')
    reloadbg(gamepath+selectedqueue[1]+'/'+selectedqueue[3],gamepath+selectedqueue[1]+'/')
    if reloadleaderboard:
        if getsetting('leaderboardtype'):
            threading.Thread(target=rleaderboard, args=(eval(get_info('beatmapids'))[selected[1]],)).start()
        else:
            rlocalleaderboard(eval(get_info('beatmapids'))[selected[1]])
    if getranky:
        threading.Thread(target=getstat, args=(get_info('beatmapsetid'),)).start()
    if mod[0]==' ':
        mod=mod[1:]
    creator=get_info('creator')
    starrating=0
    if acc:
        grabobjects(gamepath+selectedqueue[1]+'/'+eval(get_info('diffurl'))[selid])
        bpm=get_info('bpm')
        reloadpoints()
        starrating=suna(getobjects(),get_info('bpm'))
    else:
        print('No maps found')
    startani(diffsec)
    if selectedqueue[2] and reloadmusic:
        load_music(gamepath+selectedqueue[1]+'/'+selectedqueue[2],-1,fadein=1)
oh=0
ow=0