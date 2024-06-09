bpm=60000
pausedur=3
isplaying=0
def spectrum():
    global bars
    for a in range(1,len(bars)+1):
        ral=random.randint(1,100)
        bars[a-1]=ral
        render('rect', arg=(((tal)*(a-1),h-ral,(tal),ral), (255,255,255), False),borderradius=10)
def get_creation_time(item):
    item_path = os.path.join(gamepath, item)
    return os.path.getctime(item_path)
def beatmapload():
    global p2,p1,beatnowmusic,gc,speed,fbt,pausetime,isplaying,gametime,bp1,bp2,beatani,beatmaps,diffani,beattitle,fullbeatmapname,objects,diffp,betaperf,reloaddatabase,maxperf,background,ranktype,diff,diffmode,pref,level,ismusic,bpm,realid,prestart,beatsel,tick,lastms,combotime,songoffset,metadata
    if reloaddatabase:
        p1=[]
        p2=[]
        fullbeatmapname=[]
        reloaddatabase=0
        fbt=''
        beatmaps=len(os.listdir(gamepath))
        for b in sorted(os.listdir(gamepath), key=get_creation_time):
            try:
                name=str(b)[str(b).index(' ')+1:]
                if search[1] in name.lower():
                    p1.append((((cardsize//2),(size),cardsize,size)))
                    p2.append(name)
                    fullbeatmapname.append(b)
            except Exception:
                pass
        if not len(p2) and beatmaps>0:
            background=pygame.Surface((0,0))
            pygame.mixer.music.stop()
            songtitle='No beatmaps avaliable!'
    if prestart:
        if len(fullbeatmapname)!=0:
            beatsel=random.randint(1,len(fullbeatmapname))-1
        prestart=0
    if ismusic:
        #gametime=pygame.mixer.music.get_pos()
        speed=1
        gametime=(((time.time()-gc)/0.001))*speed
        if 0==1: #DISABLEEEEE
            if modsen[5]:
                speed=1.5
            elif modsen[6]:
                speed=0.5
            if not (gametime*0.001)*speed> lastms-1000:
                pygame.mixer.music.set_pos((gametime*0.001)*speed)
        pygame.mixer.music.set_volume((volvisual*0.01))
    else:
        background=pygame.Surface((0,0))
#        pygame.mixer.music.set_volume(0)
        #pygame.mixer.music.set_pos(time.time()-gametime)
        #pass
#        if gametime<0:
#            gametime=0
        #pygame.mixer.music.play(-1,(time.time()-gametime))
    try:
        if beatnowmusic:
            pausetime=time.time()+pausedur
            fbt=fullbeatmapname[beatsel]
            beatani=[Tween(begin=cross[0], end=beatsel,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
            beatani[0].start()
            diffani=[Tween(begin=-1, end=0,duration=1,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
            diffani[0].start()
            gc=time.time()
            if activity==4:
                gc+=pausedur
            ranktype=3
            gametime=0
            tick=0
            ismusic=False
            loop=-1
            if len(fullbeatmapname)!=0:
                aga=0
                if os.path.isdir(gamepath+fbt):
                    ah=os.listdir(gamepath+fbt)
                    for bop in ah:
                        if bop.endswith('.mp3') or bop.endswith('.ogg'):
                            music=bop
                            aga=1
                            break
                    if aga:
                        ismusic=True
            if ismusic:
                #if not int(time.time()-wait)<=-1:
                if 1==1:
                    isplaying=0
                    beatnowmusic=0
                    realid=fbt
                    diff=[]
                    pref=''
                    for a in ah:
                        if a.endswith('.osu'):
                            ax=re.findall(r'\[(.*?)\]', a)
                            if len(str(ax))>2:
                                diff.extend(ax)
                        if pref=='' and a.endswith('.osu'):
                            pref=a.replace('.osu','')
                            pref=pref[:pref.index('[')]
                    diffp=[]
                    for difftmp in diff:
                        beatmap=open(gamepath+fbt+'/'+pref+'['+difftmp+']'+'.osu',encoding='utf-8', errors='replace').read().rstrip('\n').split('\n')
                        general=beatmap[beatmap.index('[General]')+1:]
                        general=general[:general.index("")]
                        for a in general:
                            if "AudioFilename" in a:
                                music=a.split(': ')[1]
                        objects=len(beatmap[beatmap.index('[HitObjects]')+1:])
                        difficulty=beatmap[beatmap.index('[Difficulty]')+1:]
                        difficulty=difficulty[:difficulty.index('')]
                        metadata=beatmap[beatmap.index('[Metadata]')+1:beatmap.index('[Difficulty]')-1]
                        diffp.append((objects,difftmp))
                    diffp=sorted(diffp, key=lambda x: x[0])
                    diff=diffp
                    bp1=[]
                    bp2=[]
                    a=0
                    for b in diff: # type: ignore
                        bp1.append((((cardsize//2),size,cardsize,size))) # type: ignore
                        bp2.append(str(b[1]))
                        a+=1
#                    print(diffp)
                    #print(ids)
                    pygame.mixer.music.load(gamepath+fbt+'/'+music)
                    reloadstats()
                    betaperf=0
                    ptick=0
                    gener=0
                    perfnerf=0.00975
                    perfntot=0
                    for a in objects:
                        if int(a.split(',')[2])//100>ptick:
                            ptick=int(a.split(',')[2])//100
                            perfntot=0
                        else:
                            perfntot+=perfnerf
                        betaperf+=perfntot
                    betaperf=betaperf
                    if betaperf>1500:
                        betaperf=1500
                    lastms=int(objects[-1].split(',')[2])
                    print(isplaying)
#                    else:
#                        ranktype=
            else:
                lastms=1
                #objects=['','']
                #metadata=beatmap[beatmap.index('[Metadata]')+1:]
#            for a in beatmap[:3]:
#                print(a)
#            sys.exit()
    except Exception as err:
        print('SONG SUBSYSTEM: ',err)
        song_change(1)
    a=0
    if beatmaps>0 and ismusic:
        if activity==4 and time.time()-pausetime>=0:
            a=1
            loop=0
        elif not activity==4:
            a=1
            loop=-1
        if a and not isplaying:
            pygame.mixer.music.play(loop)
            print(isplaying)
            isplaying=1
def volchg(t):
    global vol,voltime,volani
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
