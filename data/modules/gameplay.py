
from data.modules.input import get_input
from data.modules.colours import maincolour
from data.modules.settings import getsetting,setsetting
from data.modules.audio import load_music,get_pos,music_control
from data.modules.beatmap_processor import get_info,getobjects,getpoint,getkeycount,getkeypos
from data.modules.onlineapi import getleaderboard,submit_score,issubmiting,setsubmit,getsubmitstatus
from data.modules.bootstrap import getimg,getactivity,transitionprep,clockify,gamepath
import data.modules.renderapi as renderapi
import pygame,time,threading
from random import randint
from tweener import *
perfect=80
great=perfect*2
ok=perfect*3
miss=0
kdur=250
accuracy=100
notecolour=(48, 183, 255)
maxhealth=110
health=maxhealth
hittext='PERFECT','GREAT','MEH','MISS'
hitcolour=(100, 120, 200),(100, 200, 100),(200, 200, 100),(200, 100, 100)
def iscatched(keymap,block,isauto,ob,fir,h):
    from data.modules.songselect import modsen
    lean=(perfect,great,ok,miss,100) # Last one is for Auto
    tick=0
    agree=1
    if ob==fir or isauto:
        agree=True
    else:
        agree=False
    hitrange=h-60
    if block>=h-lean[3]:
        lastcall=True
        tick=3
    elif (block>=hitrange-lean[0] and block<=hitrange+keymap[0][3]+lean[0] and agree and not isauto) or (block>=hitrange-lean[4] and block<=hitrange+keymap[0][3]+lean[0] and agree and isauto):
        lastcall=True
        tick=0
    elif block>=hitrange-lean[1] and block<=hitrange+keymap[0][3]+lean[1] and not isauto and agree and not modsen[5]:
        lastcall=True
        tick=1
    elif block>=hitrange-lean[2] and block<=hitrange+keymap[0][3]+lean[2] and not isauto and not modsen[5]:
        lastcall=True
        tick=2
    else:
        lastcall=False
    tim=block
    return (lastcall,tick,tim)

def reset_score():
    global points,combo,ncombo,maxcombo,hits,clickedkeys, ncombo,keys, combotime, accuracy, timetaken,health,keyslight,pos
    e=getkeypos()
    if e:
        pos=e
    else:
        pos=(64,192,320,448) # Keys
    keyslight=[Tween(begin=0) for a in range(0,getkeycount())]
    points = 0
    ncombo = 0
    health=10
    timetaken=time.time()
    combo = 0
    ncombo = 0
    maxcombo = 0
    clickedkeys = []
    hits = [0,0,0,0]
    keys = [0 for a in range(0,getkeycount())]
    combotime = time.time()
    accuracy = 0

def song_progress(screen,start,end,w,h):
    if not end<1:
        slop=(start/end)
        if slop>1:
            slop=1
        elif slop<0:
            slop=0
        endtime=clockify(int((end-start))).replace('-','')
        tmp = renderapi.getfonts(0).render('-'+endtime,True,(255,255,255))
        out = tmp.get_rect()
        screen.blit(tmp,(w-25-out[2],h-50))
        tmp = renderapi.getfonts(0).render(clockify(int(start)),True,(255,255,255))
        screen.blit(tmp,(25,h-50))
        pygame.draw.rect(screen,(50,50,50),pygame.Rect(10,h-20,w-20,10))
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(10,h-20,slop*(w-20),10))
def showplayfield(screen,pos,keymap,bypass=False):
    linecol=(80,80,100)
    h=screen.get_height()
    count=getkeycount()
    space=(keymap[0][2]*count//2)
    pygame.draw.rect(screen,(50,50,50),(pos[0]-space,h-60+pos[1]-10,keymap[0][2]*count,10)) # Judgement Line
    col=(10,30),(20,40)
    for a in range(1,count+1):
        b=a-1
        if a>1 and a<4:
            bcol=col[1]
        else:
            bcol=col[0]
        co=(100,int(100+(20*keyslight[b].value)),int(100+(120*keyslight[b].value)))
        cb=(80,int(80+(20*keyslight[b].value)),int(80+(120*keyslight[b].value)))
        cc=(40,int(40+(bcol[0]*keyslight[b].value)),int(40+(bcol[1]*keyslight[b].value)))
        pygame.draw.rect(screen,(cc),(keymap[b][0]-((keymap[0][2]*getkeycount()//2))+pos[0],0,keymap[b][2],keymap[b][3]+(h-100)))
        pygame.draw.rect(screen,(cb),(keymap[b][0]-((keymap[0][2]*getkeycount()//2))+pos[0],h-60+pos[1],keymap[b][2],keymap[b][3]))
        pygame.draw.rect(screen,(co),(keymap[b][0]-((keymap[0][2]*getkeycount()//2))+pos[0],h-60+pos[1]+(10*-keyslight[b].value),keymap[b][2],keymap[b][3]))
#        tmp = renderapi.getfonts(0).render(str(a),True,(255,255,255))
#        screen.blit(tmp,(keymap[b][0]+pos[0],h-60+pos[1]))
        #render('rect', arg=(), cb, False),borderradius=0) # Judgement Block
        #render('rect', arg=((()), co, False),borderradius=0) # Judgement Block
#        if a==4:
#            pygame.draw.line(screen,linecol,(keymap[-1][0]+pos[0]+100,0+pos[1]),(keymap[-1][0]+pos[0]+100,keymap[-1][1]+pos[1]+30-1))
#        pygame.draw.line(screen,linecol,(keymap[-1][0]+pos[0]+100,0+pos[1]),(keymap[-1][0]+pos[0]+100,keymap[-1][1]+pos[1]+30-1))
        #render('line',arg=((keymap[b][0]+pos[0],0+pos[1]),linecol,(keymap[b][0]+pos[0],keymap[b][1]+pos[1]+noteheight-1)))
objecon=0
def resetcursor():
    global objecon
    objecon = 0
def main(screen,w,h):
    global objecon, points,combo,maxcombo,hits,clickedkeys,judgewindow, ncombo,keyslight,keys, combotime,accuracy,health,firstobject
    if getactivity() == 5:
        from data.modules.songselect import modsen,reload_map,getmaxpoints,selected,mods,get_mods,getmult
        for a in keyslight:
            a.update()
        screen.fill((20,20,20))
        clicked=0
        length=get_info('lengths')[selected[1]]
        fieldpos = (w//2,0) # Gameplay field
        if health<0:
            health=maxhealth
            transitionprep(2)
        elif health>=maxhealth:
            health=maxhealth
        t1=0.01
        maxt1=0.15
        t1=t1*(combo+ncombo+0.01)
        if t1>=maxt1:
            t1=maxt1
        tmp=0.1
        sretemplate=(tmp-(time.time()-combotime))/tmp
        sre=(sretemplate)*20    
        if sre<=0:
            sre=0
        points=getpoint(hits[0],hits[1],hits[2],hits[3],getmult(),combo,type=float)
        maxpoints=getmaxpoints()
        if points>maxpoints:
            points=maxpoints
        if maxpoints!=0:
            end=int((points/maxpoints)*(1000000*getmult()))
        else:
            end=0
        maxc=hits[0]+hits[1]+hits[2]+hits[3]
        if not maxc<1:
            accuracy=round(((hits[0]+(hits[1]/2)+(hits[2]/3))/(maxc))*100,2)
        else:
            accuracy=100
        keymap=tuple((100*id,h-30,100,30) for id in range(0,getkeycount()))
        showplayfield(screen,fieldpos,keymap)
        objects=getobjects()
        ti=get_pos()
        keyqueue=[]
        if objects:
            for ob in objects[objecon:255+objecon]:
                obid=1
                block=ti-int(ob[2])+h
                if (block <=h+100 and block>=-40 and not modsen[2]) or (block <=h+100 and block>=h//2 and modsen[2]):
                    notfound=True
                    if obid==1:
                        if not end*1000000 >=999000 and (modsen[0] and health>1):
                            health-=t1
                    for kik in range(0,len(pos)):
                        if int(ob[0])==int(pos[kik]):
                            barpos=kik
                            notfound=False
                            break
                    if notfound:
                        print('!!')
                        for kik in range(0,4):
                            if int(ob[0])>=512-(128*(kik+1)):
                                barpos=kik
                                break
                    
                    if not (barpos,int(ob[2])) in clickedkeys:
                        if not modsen[1] or modsen[1] and block<=h//2:
                            bar=getimg('note.png')
                            if bar:
                                keyoffset=bar.get_rect()[3]
                                screen.blit(bar,(fieldpos[0]-((keymap[0][2]*getkeycount()//2))+keymap[barpos][0],block-keyoffset))
                            else:
                                pygame.draw.rect(screen,notecolour,(fieldpos[0]-((keymap[0][2]*getkeycount()//2))+keymap[barpos][0],block-keymap[0][3],keymap[0][2],keymap[0][3]))
                    if obid==1:
                        firstobject=int(block)
                        obid+=1

                    judge=iscatched(keymap,block,modsen[0],firstobject,obid,h)

                    if modsen[0]:
                        if judge[0]:
                            keys[kik]=1
                    if (judge[0] and keys[kik]) or judge[1]==3: 
                        hit=judge[1]
                        clicked=1
                        keyqueue.append((barpos,int(ob[2])))



                    # Saves FRAMES
                    if pygame.Rect.colliderect(pygame.Rect(0,h+50,w,60),pygame.Rect(0,block,w,30)):
                        objecon+=1
        if clicked:
            for notes in keyqueue:
                if not (notes[0],int(notes[1])) in clickedkeys:
                    if hit==3:
                        health-=t1*(ncombo+combo)
                    else:
                        health+=10
                    try:
                        judgewindow=hit
                    except Exception:
                        judgewindow=hit
                    hits[hit]+=1
                    clickedkeys.append((notes[0],int(notes[1])))
                    if not hit==3:
                        combo+=1
                        if ncombo>0:
                            ncombo-=1
                        if combo>maxcombo:
                            maxcombo=combo
                        combotime=time.time()
                        try:
                            t=a.split(':')[-1]
                            if not t=='' and getsetting('hitsound'):
                                pygame.mixer.Sound(gamepath+get_info('raw')+'/'+str(t)).play()
                                print('Played',t)
                        except Exception:
                            pass
                    else:
                        ncombo+=1
                        combotime=time.time()
                        combo=0
                        #health-=t1


        for a in range(0,getkeycount()):
            if keys[a]:
                keyslight[a]=Tween(begin=1, end=0,duration=kdur,easing=Easing.BOUNCE,easing_mode=EasingMode.OUT)
                keyslight[a].start()
                keys[a]=0
        if length:
            if not music_control(4) and get_pos()>=0:
                music_control(0)
            if  get_pos()>=length+1000:
                if not getsubmitstatus():
                    setsubmit(1)
                    threading.Thread(target=submit_score,args=(int(points),maxcombo,get_info('beatmapids')[selected[1]],get_info('beatmapsetid'),hits[0],hits[1],hits[2],hits[3],get_info('maps')[selected[1]],mods,int(getmaxpoints()),int(time.time()-timetaken),)).start()
                transitionprep(9)
            if getsetting('hidegamehud'):
                song_progress(screen,get_pos(),length+1000,w,h)
        if getsetting('hidegamehud'):
            pygame.draw.rect(screen,maincolour[0],pygame.Rect(0,0,w,55),border_bottom_left_radius=20,border_bottom_right_radius=20)
            pygame.draw.rect(screen,maincolour[1],pygame.Rect(w//2-200,19,401,61),border_radius=20)
            renderapi.center_text(screen,str(end),(w//2-200,30,401,60),'score',(255,255,255))
            renderapi.center_text(screen,str(accuracy)+'% ',(w//2-200,82,200,20),'',(255,255,255))
            renderapi.center_text(screen,format(int(points),',')+'pp',(w//2,82,200,20),'',(255,255,255))
            tmp=(health/100)*400
            if tmp<0:
                tmp=0
            elif tmp>400:
                tmp=400
            pygame.draw.rect(screen,(0,180,0),(w//2-200,5,tmp,10),border_radius=10)
            get_mods(screen,(20,20))
        if combo!=0:
            kek=(w//2-200,100,400,100)
            comboo=str(format(int(combo),','))
            if sre:
                renderapi.center_text(screen,comboo,(kek[0]-sre,kek[1],kek[2],kek[3]),'score',(255,0,0))
                renderapi.center_text(screen,comboo,(kek[0]+sre,kek[1],kek[2],kek[3]),'score',(0,0,255))
                renderapi.center_text(screen,comboo,(kek[0],kek[1]+sre,kek[2],kek[3]),'score',(0,255,0))
                renderapi.center_text(screen,hittext[judgewindow],(kek[0],kek[1]+60,kek[2],kek[3]),'score',hitcolour[judgewindow])
            renderapi.center_text(screen,comboo,(kek),'score',(255,255,255))
            

#        tmp = renderapi.getfonts(0).render(str(combo),True,(255,255,255))
#        screen.blit(tmp,(10,10))
## Leaderboard Section
        lead=getleaderboard()
        if getsetting('leaderboard') and len(lead)>0:
            players=1
            t=1
            if not modsen[0]:
                user=getsetting('username')
            elif getsetting('username')==None:
                user='Guest'
            else:
                user='Qlutina'
            current={'username': user,'score': end,'points': points,'combo':maxcombo,'current': True}
            tmpl = lead + [current]
            ranking=51
            for tmp in sorted(tmpl, key=lambda x: x['points'],reverse=True):
                if tmp['username'] in (getsetting('username'),user) and "current" in tmp:
                    pcolour=maincolour[0]
                    pcol=(252, 255, 166)
                elif tmp['username'] in (getsetting('username'),user):
                    pcolour=maincolour[1]
                    pcol=(166, 207, 255)
                else:
                    pcol=(255,255,255)
                    pcolour=maincolour[2]
                if tmp['username']==user:
                    ranking=players
                if players<=5 or players==ranking:
                    pygame.draw.rect(screen,pcolour,pygame.Rect(-30,65+(50*(t)),225,50),border_bottom_right_radius=10,border_top_right_radius=10)
                    screen.blit(renderapi.getfonts(0).render(tmp['username'],True,pcol),(20, 70+(50*t)))
                    screen.blit(renderapi.getfonts(1).render('#'+str(players)+' '+format(tmp['score'],','),True,pcol),(20, 95+(50*t)))
#                    render('rect', arg=((-30,65+(50*(t)),225,50), pcolor, False),borderradius=10)
#                    render('text',text=,arg=((20, 70+(50*(t))),pcol)) #'#'+str(players)+' '+
#                    render('text',text=,arg=((20, 95+(50*(t))),pcol,'min'))
#                    render('text',text='('+str(int(tmp['combo']))+'x)',arg=((180, 95+(50*(t))),pcol,'min','rtl'))
                    t+=1
                players+=1

## Input

        for event in get_input():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,pygame.K_q):
                    transitionprep(2)
                elif event.key == pygame.K_BACKQUOTE:
                    reload_map()
                elif event.key == pygame.K_F3:
                    setsetting('hidegamehud',not getsetting('hidegamehud'))
                for a in range(0,getkeycount()):
                    if event.unicode  ==  getsetting('Key'+str(a+1)):
                        keys[a]=1