notecolour=(48, 183, 255)
def getpoint(perfect,good,meh,bad,multiplier,combo=1,type=int):
    multiplier=multiplier
    tmp=(((perfect*perfbom)+(good*(perfbom/2))+(meh*(perfbom/3))-(bad*(perfbom*2)))*multiplier)
    tmp+=perfbom*combo
    return type(tmp)
def clockify(clo):
    minraw=int(clo/60)
    if minraw>98:
        minraw=99
    min="{:02d}".format(int(minraw))
    sec="{:02d}".format(int(clo-(60*minraw)))
    return str(min)+':'+str(sec)
def song_progress():
    if not lastms<1:
        slop=(gametime/lastms)
        if slop>1:
            slop=1
        render('text',text=clockify(int(gametime//1000)/speed),arg=((25,h-50),forepallete))
        render('text',text='-'+clockify(int((lastms-gametime)//1000)/speed),arg=((w-25,h-50),forepallete,'rtl'))
        render('rect', arg=((10,h-20,w-20,10), (50,50,50), False),borderradius=10)
        render('rect', arg=((10,h-20,slop*(w-20),10), (255,255,255), False),borderradius=10)
def iscatched(block,isauto,ob,fir,id):
    lean=(perfect,great,ok,miss,20) # Last one is for Auto
    tick=0
    agree=1
#    if ob==fir:
#        agree=True
#    else:
#        agree=False
    if block>=h-lean[3]:
        lastcall=True
        tick=3
    elif (block>=keymap[0][1]-lean[0] and block<=keymap[0][1]+keymap[0][3]+lean[0] and agree and not isauto) or (block>=keymap[0][1]-lean[4] and block<=keymap[0][1]+keymap[0][3]+lean[0] and agree and isauto):
        lastcall=True
        tick=0
    elif block>=keymap[0][1]-lean[1] and block<=keymap[0][1]+keymap[0][3]+lean[1] and not isauto and agree:
        lastcall=True
        tick=1
    elif block>=keymap[0][1]-lean[2] and block<=keymap[0][1]+keymap[0][3]+lean[2] and not isauto :
        lastcall=True
        tick=2
    else:
        lastcall=False
    tim=block
    return (lastcall,tick,tim)
def showplayfield(pos,bypass=False):
    for a in range(1,5):
        b=a-1
        mopa=(0.1-(time.time()-keyslight[b]))/0.1
        if mopa<0:
            mopa=0
        co=(100,int(100+(20*mopa)),int(100+(120*mopa)))
        render('rect', arg=(((keymap[b][0]+pos[0],keymap[b][1]+pos[1],keymap[b][2],keymap[b][3])), co, False),borderradius=0) # Judgement Block
        if a==4:
            render('line',arg=((keymap[-1][0]+pos[0]+100,0+pos[1]),(255,255,255),(keymap[-1][0]+pos[0]+100,keymap[-1][1]+pos[1]+noteheight)))    
        render('line',arg=((keymap[b][0]+pos[0],0+pos[1]),(255,255,255),(keymap[b][0]+pos[0],keymap[b][1]+pos[1]+noteheight)))
    render('rect', arg=((keymap[0][0]+pos[0],keymap[0][1]-10+pos[1],keymap[0][2]*4,10), (100,140,220), False),borderradius=0) # Judgement Line

def game():
    global activity,timestep,debugmode,ncombo,replaystore,accuracy,beatnowmusic,kiai,unstablerate,fpsmode,score,scorew,keyspeed,bgcolour,totperf,totscore,objecon,healthtime,health,ranking,oldupdatetime,t,tip,gametime,combo,sre,combotime,sre,hits,last,stripetime,tmp,pptime,pptmp,ppcounter,perf
    if activity==4:
        if bgcolour>=1:
            bgcolour-=1
        playfield=(maxt(20,bgcolour),maxt(20,bgcolour),maxt(20,bgcolour))
        screen.fill(playfield)
        tmp=0.1
        sretemplate=(tmp-(time.time()-combotime))/tmp
        sre=(sretemplate)*20
        if sre<=0:
            sre=0
        #if gametime<0:
        #    pygame.mixer.music.play(-1,0)

        b=0
        perf=getpoint(hits[0],hits[1],hits[2],hits[3],scoremult,combo,type=float)
        if perf>maxperf:
            perf=maxperf
        maxc=hits[0]+hits[1]+hits[2]+hits[3]
        if not maxc<1:
            accuracy=round(((hits[0]-(hits[1]/2)-(hits[2]/3)-(hits[3]/4))/(maxc))*100,2)
        else:
            accuracy=100
        #accuracy=100
        if int(maxperf)!=0:
            end=(perf/maxperf)*(scoremult*1000000)
        else:
            end=0
#        end=(300*hits[0])+(100*hits[1])+(50*hits[2])
#        end*=scoremult
#        end*=combo//2
        if health<0:
            health=100
            transitionprep(3)
        elif health>=110:
            health=110
        t1=0.01
        maxt1=0.15
        t1=t1*(combo+ncombo+0.01)
        if t1>=maxt1:
            t1=maxt1
        ob=0
        score=int(end*(1000000*scoremult))
        score=int(end)
        temp=h//2+int(gametime)
        showplayfield(fieldpos)
        clicked=0
        hit=-1
        tip=1
        hidden=0
        b=0
        for a in unstablerate[::-1]:
            break
            if time.time()-a[0]>0.5:
                unstablerate.remove(a)
            if b>16:
                break
            else:
                render('rect', arg=((keymap[3][0]+110,keymap[0][1]-50-(25*b),20*(1+b),20), hitcolour[a[1]], False))
                render('rect', arg=(((fieldpos[0]//2)-30-(20*(b)),keymap[0][1]-50-(25*b),20*(b+1),20), hitcolour[a[1]], False))
                b+=1
        for a in objects[objecon:maxobjec+objecon]:
            tok=a.split(',')
            #if tok[2]==firstobject:
            block=temp-(int(tok[2]))+(h//2)
            if (block <=h+100 and block>=-40 and not modsen[2]) or (block <=h+100 and block>=h//2 and modsen[2]):
                if ob==0:
                    if not end*1000000 >=999000 and (modsen[0] and health>1):
                        health-=t1
                ob+=1
                if ob==1:
                    #if not keys:
                    firstobject=int(block)
                notfound=True
                for kik in range(1,len(pos)+1):
                    if int(tok[0])==pos[kik-1]:
                        keypos=keymap[kik-1][0]
                        notfound=False
                        break
                if notfound:
                    for a in range(1,6):
                        if a-1>=4:
                            ax=3
                        else:
                            ax=a-1
                        if int(tok[0])>=512-(128*(a-1)):
                            keypos=keymap[ax][0]
                            break
#                if modsen[1]:
#                    notecolour=(mint(int(playfield[0]),int((500/block)*48)), mint(int(playfield[1]),int((500/block)*183)), mint(int(playfield[2]),int((500/block)*255)))
#                else:
                if not (keypos,int(tok[2])) in barclicked:
#                    if not modsen[1]:
#                        if tip:
#                            render('rect', arg=((keypos,block-30,100,30), (255,0,0), False),borderradius=0)
#                        else:
                    keyoffset=30
                    if not modsen[1] or modsen[1] and block<=h//2:
                        if kiai:
                            render('rect', arg=((keypos+fieldpos[0],block-(keyoffset)-(60*flashylights)+fieldpos[1],notewidth,noteheight), (255,0,0), False),borderradius=0)
                        render('rect', arg=((keypos+fieldpos[0],block-(keyoffset)+fieldpos[1],notewidth,noteheight), (notecolour), False),borderradius=0)
                    #render('text',text=block,arg=((keypos,block-30),(255,255,255)))
                    tip=0
                judge=iscatched(block,modsen[0],block,firstobject,ob)
                if modsen[0]:
                    if judge[0]:
                        keys[kik-1]=1
                        if settingskeystore['sreplay']:
                            replaystore.append(str(gametime)+';'+str(keys[0])+';'+str(keys[1])+';'+str(keys[2])+';'+str(keys[3]))
                        keyslight[kik-1]=time.time()
                    else:
                        keys[kik-1]=0
                if (judge[0] and keys[kik-1]) or judge[1]==3: 
                    hit=judge[1]
                    clicked=1
                    if keys[kik-1]:
                        keys[kik-1]=0
                    stripetime.append((keypos,int(tok[2])))
                    #print((keypos,int(tok[2])))
                if pygame.Rect.colliderect(pygame.Rect(0,h+45,w,20),pygame.Rect(keypos,block,100,30)):
                    objecon+=1
            #print(time.time(),firstobject,tok[2])
        if clicked:
            for notes in stripetime:
                if not (notes[0],int(notes[1])) in barclicked:
                    if hit==3:
                        health-=t1
                    else:
                        health+=10
                    hits[hit]+=1
                    bgcolour+=1
                    barclicked.append((notes[0],int(notes[1])))
                    ton=(time.time(),hit)
                    unstablerate.append(ton)
                    if not hit==3:
                        combo+=1
                        if ncombo>0:
                            ncombo-=1
                        combotime=time.time()
                        t=a.split(':')[-1]
                        if not t=='' and settingskeystore['hitsound']:
                            pygame.mixer.Sound(gamepath+realid+'/'+str(t)).play()
                            print('Played',t)
                    else:
                        ncombo+=1
                        combotime=time.time()
                        combo=0
                        health-=t1
            stripetime=[]
        
        if settingskeystore['leaderboard'] and len(leaderboard)>0:
            players=1
            t=1
            if not modsen[0]:
                user=settingskeystore['username']
            elif settingskeystore['username']==None:
                user='Guest'
            else:
                user='Qlutina'
            current={'username': user,'score': score,'points': perf,'current': True}
            tmpl = leaderboard + [current]
            ranking=51
            #playboard[len(playboard)-1]=(username,(255,255,0),int(end*1000000))
            for tmp in sorted(tmpl, key=lambda x: x['points'],reverse=True):
                if tmp['username'] in (settingskeystore['username'],user) and "current" in tmp:
                    pcolor=blend(opacity,50)
                    pcol=(252, 255, 166)
                elif tmp['username'] in (settingskeystore['username'],user):
                    pcolor=blend(opacity,20)
                    pcol=(166, 207, 255)
                else:
                    pcol=forepallete
                    pcolor=blend(opacity,20)
                if tmp['username']==user:
                    ranking=players
                if players<=5 or players==ranking:
                    render('rect', arg=((-30,65+(50*(t)),225,50), pcolor, False),borderradius=10)
                    #render('text',text='#'+str(players),arg=((20, 80+(50*(t))),(pcolor[0]-20,pcolor[1]-20,pcolor[2]-20)))
                    render('text',text=tmp['username'],arg=((20, 70+(50*(t))),pcol)) #'#'+str(players)+' '+
                    render('text',text='#'+str(players)+' '+format(tmp['score'],','),arg=((20, 95+(50*(t))),pcol,'min'))
                    t+=1
                players+=1
        if score<0:
            t=(255,0,0)
        else:        
            t=forepallete
        render('rect', arg=((0,-20,w,55), (50,50,60), False),borderradius=20)
        render('rect', arg=((w//2-200,19,401,61), (50,50,80), False),borderradius=20)
        render('text',text=format(score,','),arg=((20, 20),t,'grade','center'),relative=(w//2-200,22,400,60))
        render('text',text=str(accuracy)+'% '+format(int(perf*(accuracy*0.01)),',')+'pp',arg=((20, 170),forepallete,'center'),relative=(w//2-200,82,400,20))
        get_mods((20,20))
        if combo!=0:
            kek=(w//2-(notewidth*2),100,400,100)
            comboo=str(format(int(combo),','))
            if sre:
                try:
                    judgewindow=judge[1]
                except Exception:
                    judgewindow=0
                render('text',text=comboo,arg=((0,0),(255,0,0),'grade','center'),relative=(kek[0]-sre,kek[1],kek[2],kek[3]))
                render('text',text=comboo,arg=((0,0),(0,0,255),'grade','center'),relative=(kek[0]+sre,kek[1],kek[2],kek[3]))
                render('text',text=comboo,arg=((0,0),(0,255,0),'grade','center'),relative=(kek[0],kek[1]+sre,kek[2],kek[3]))
                render('text',text=hittext[judgewindow],arg=((0,0, h-80-sre),hitcolour[judgewindow],'grade','center'),relative=(kek[0],kek[1]+60,kek[2],kek[3]))
            render('text',text=comboo,arg=((0,0, h-80-sre),forepallete,'grade','center'),relative=kek)
        #render('text',text=h//2+gametime-(int(objects[0].split(',')[2])),arg=((20, 80),forepallete))
        render('line',arg=((0,h-miss),(255,255,255),(w,h-miss)))
#        render('text',text='Key Speed: '+str(keyspeed)+' ('+str(0)+'ms)',arg=((20, 70),forepallete))
        render('rect', arg=((w//2-200,5,400,10), (20,20,20), False),borderradius=10)
        #render('rect', arg=((w//2-200,50,((maxscore-score)/maxscore)*400,20), (255,0,0), True),borderradius=10)
        tmp=(health/100)*400
        if tmp<0:
            tmp=0
        elif tmp>400:
            tmp=400
        render('rect', arg=((w//2-200,5,tmp,10), (0,180,0), False),borderradius=10)
        fon=0
        #for a in timings[timestep]: # 7 == Kiai
        tim=timings[timestep].split(',')
#        print(tim,gametime)
        if gametime>=int(float(tim[0])) and not fon:
#            print(timestep,a)
            if not timestep+1>len(timings)-1:
                timestep+=1
            if int(tim[7])==1:
                kiai=1
            else:
                kiai=0
            fon=1
        tim=temp-(int(float(tim[0])))+(h//2)
        if tim <=h+100 and tim>=-40:
            render('rect', arg=((w//2-(notewidth*2)-100,tim,keymap[0][2]*6,5), (255,255,255), False),borderradius=20)
            
#        tmp=end*400
#        if tmp<0:
#            tmp=0
#        elif tmp>400:
#            tmp=400
#        render('rect', arg=((w//2-200,5,tmp,10), (0,150,0), False),borderradius=10)
#        for a in range(1,len(keys)+1):
#            if keys[a-1]:
                
        song_progress()
        if "tornney" in settingskeystore:
            render('text',text=settingskeystore['username'],arg=((w-20, h-120),forepallete,'grade','rtl'))
        if  gametime>=lastms+1000:# or combo>49:
            render('rect', arg=((0,h//2-50,w,100), (255,255,255), False))
            render('text',text='Loading...',arg=((20, 20),(0,0,0),'grade','center'),relative=(w//2-100,h//2-50,200,100))
            pygame.display.update()
            if settingskeystore['sreplay']:
                with open(replaypath+'replay-'+str(str(time.time())+'-'+str(settingskeystore['username']))+'-'+str(beatmapsetid)+'-'+str(beatmapid),'w') as x:
                    x.write('#'+str(gamename)+'-'+str(gamever)+'\n'+str(settingskeystore['username'])+';'+str(hits[0])+';'+str(hits[1])+';'+str(hits[2])+';'+str(hits[3])+';'+str(mods)+'\n')
                    for a in replaystore:
                        x.write(a+'\n')
            submit_score(perf,combo,other=str(beatmapid)
                             +';'+str(beatmapsetid) # BeatmapSet ID
                             +';'+str(hits[0])+';' # PERFECT / OUTRAGOUS
                             +str(hits[1])+';' #GREAT
                             +str(hits[2])+';' # OK
                             +str(hits[3])+';' # BAD
                             +str(diffmode)+';' # Difficulty
                             +str(mods)+';' # Mods
                             +str(maxperf)+';' # Max Points
                             +str(int(time.time()-timetaken)))
            activity=5

