import requests,threading,re
from urllib.parse import unquote
lvrating=0
def bpmparse(bpm):
    return bpm.split(',')[1]
def reloadbg():
    global background,bump,sc
    try:
        b=0.50
        background=pygame.image.load(gamepath+fullbeatmapname[beatsel]+'/'+backgroundev).convert_alpha()
        sc=background.get_rect()[2],background.get_rect()[3]
        background=pygame.transform.scale(background, (w,h))
        background.fill((255*b, 255*b, 255*b,128), special_flags=pygame.BLEND_RGBA_MULT)
    except Exception:
        pass
def reloadstats(reloadleaderboard=False):
    global objects,difficulty,background,backgroundev,songtitle,metadata,timings,lvrating,levelrating,levelcol,bpm,songoffset,maxperf,scoremult,ismulti,beattitle,perfect,great,ok,diffmode,beatmapid,beatmapsetid
    diffmode=diff[diffcon][1]
    beatmap=open(gamepath+fullbeatmapname[beatsel]+'/'+pref+'['+diffmode+']'+'.osu').read().rstrip('\n').split('\n')
    objects=beatmap[beatmap.index('[HitObjects]')+1:]
    b=0
    lvrating=0
    background=pygame.surface.Surface((0,0))
    if modsen[4]:
        print('RND MODE')
        lol=0
        tmp=''
        for a in objects:
            tmp=''
            tok=a.split(',')[1:]
            for b in tok:
                tmp+=','+str(b)
            key=randint(1,len(pos))-1
            objects[lol]=str(pos[key])+tmp
            lol+=1
    events=beatmap[beatmap.index('[Events]')+1:]
    events=events[:events.index("")]
    backgroundev=events[events.index('//Background and Video events')+1]
    if backgroundev[:3]=='0,0':
        backgroundev=backgroundev.split(',')[2].rstrip('"')[1:]
    reloadbg()
    difficulty=beatmap[beatmap.index('[Difficulty]')+1:]
    keycheck=int(float(difficulty[1].replace('CircleSize:','')))
#    if keycheck!=4:
#        print('This Game only supports ONLY 4 Keys')
#        if len(bp2)>1:
#            diff_change(1)
#        else:
#            song_change(1)
    difficulty=difficulty[:difficulty.index('')]
    metadata=beatmap[beatmap.index('[Metadata]')+1:beatmap.index('[Difficulty]')-1]
    beatmapid=None
    beatmapsetid=None
    for a in metadata:
        if 'BeatmapID' in a:
            beatmapid=int(a.replace('BeatmapID:',''))
        elif 'BeatmapSetID' in a:
            beatmapsetid=int(a.replace('BeatmapSetID:',''))
    beattitle=p2[beatsel].replace('\n','-')+' ['+str(diffmode)+']'
    songtitle=metadata[2].split(':')[1]+' - '+metadata[0].split(':')[1]
    threading.Thread(target=getstat).start()
    threading.Thread(target=rleaderboard).start()
    timingst=beatmap[beatmap.index('[TimingPoints]')+1:]
    timings=[]
    for a in timingst:
        if not len(a)<2:
            timings.append(a)
        else:
            break
    bpm=float(bpmparse(timings[0]))
    songoffset=float(beatmap[beatmap.index('[TimingPoints]')+1:][0].split(',')[0])
    scoremult=1
    inc=0.5
    inf=0.1
    perfect=80
    #perfect=60
    great=perfect*2
    ok=perfect*3
    ismulti=modsen[4]
    for a in range(2,len(modsen)+1):
        if modsen[a-1] and a==2:
            scoremult+=inc*3
        elif modsen[a-1] and not a in (4,5,7,8):
            scoremult+=inc
        elif modsen[a-1] and (a in (4,7)):
            scoremult/=inc*4
        elif modsen[a-1] and a==8:
            scoremult*=8
    lvt=0
    lvy=0
    for a in  objects:
        tmp=a.split(',')
        bartime=int(tmp[2])//100
        if bartime!=lvt:
            lvt=bartime
            lvy=0
        else:
            lvy+=1

        lvrating+=0.01*lvy
    lvrating=round(lvrating,2)*scoremult
    if lvrating>=120:
        levelcol=rankdiffc[-1]
    elif lvrating>=15:
        levelcol=rankdiffc[3]
    elif lvrating>=9:
        levelcol=rankdiffc[2]
    elif lvrating>=6:
        levelcol=rankdiffc[1]
    elif lvrating<=5:
        levelcol=rankdiffc[0]
    levelrating=rankdiff[rankdiffc.index(levelcol)]
    maxperf=getpoint(len(objects),0,0,0,scoremult,combo=len(objects))
def rleaderboard():
    global leaderboard
    leaderboard=[]
    f=requests.get(settingskeystore['apiurl']+'api/getleaderboard?'+str(beatmapid))
    leaderboard=f.json()
def getrank(id):
    if id==3 or id==4:
#        print(rankmodes[2][0])
        return 2
    if id==-1:
#        print(rankmodes[2][0])
        return 2
    elif id>0:
        return 0
    else:
#        print(rankmodes[1][0])
        return 1
def getstat():
    global ranktype,getpoints,leaderboard
    x=1
    success=0
    while x<4 and not success:
        try:
            tmp=''
            with requests.get(beatmapapi+'s/'+str(beatmapsetid),headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=3, stream=True) as f:
                tmp+=f.text
            f=json.loads(tmp)['found']
            f=f['ranked']
#            print(f)
            ranktypetmp=int(f)
            success=1
        except Exception:
            #print(error,'(Returning as Unranked)')
            x+=1
            ranktypetmp=-99
#    if len(leaderboard)>0:
#        print(f.json(),'> Leaderboard')
#    else:
#        print('No Leaderboard')
#    for a in leaderboard:
#        print(a)
    #ranktypetmp=1
    getpoints=0
    #if id!=None:
#        print(ranktypetmp)
    ranktype=getrank(ranktypetmp)
def resetscore():
    global score,ncombo,barclicked,prevrank,timestep,replaystore,unstablerate,timetaken,perf,scorew,kiai,bgcolour,objecon,combo,sre,health,healthtime,combotime,hits,last,stripetime,ppcounter,pptime,pptmp,modshow,ranking
    last=0
    ncombo=0
    prevrank=totrank
    unstablerate=[]
    timestep=0
    healthtime=time.time()
    timetaken=time.time()
    combo=0
    replaystore=[]
    kiai=0
    health=100
    stripetime=[]
    objecon=0
    pptime=time.time()
    pptmp=0
    modshow=False
    ppcounter=0
    if activity==4:
        bgcolour=235
    sre=0
    combotime=0
    hits=[0,0,0,0]
    score=0
    scorew=score
    perf=0
    barclicked=[]
def change_diff():
    global diffcon,beatnowmusic
    if not diffcon+1>=len(diff):
        diffcon+=1
    else:
        diffcon=0
def song_change(switch):
    global beatsel,beatnowmusic,diffcon,cross
    if len(p2):
        if not switch:
            if not beatsel-1<=-1:
                beatsel-=1
            else:
                beatsel=len(p2)-1
        else:
            if not beatsel+1>=len(p2):
                beatsel+=1
            else:
                beatsel=0
        beatnowmusic=1
        diffcon=0
        cross[1]=0
def diff_change(switch):
    global beatsel,beatnowmusic,diffcon,diffani
    if not switch:
        if not diffcon-1<=-1:
            diffcon-=1
        else:
            diffcon=len(diff)-1
    else:
        if not diffcon+1>=len(diff):
            diffcon+=1
        else:
            diffcon=0
    reloadstats()
    diffani=[Tween(begin=cross[1], end=diffcon,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
    diffani[0].start()
def get_rank(num):
    #crok=256*oneperf
    crok=oneperf/2
    totrank=(crok+1)-int((num/oneperf)*crok)
    return int(totrank)
def reloadprofile():
    global totperf,totscore,totrank,totacc,issigned,successfulsignin,restricted,level,qlutaerror
#    for a in pend:
    if settingskeystore['username']!='':
        try:
            if not successfulsignin:
                f=requests.get(settingskeystore['apiurl']+'api/chkprofile?'+str(settingskeystore['username'])+'?'+str(settingskeystore['password']),headers={'User-Agent': 'QluteClient-'+str(gamever)},timeout=5)
                cache=json.loads(f.text)
                if int(cache['success'])==1:
                    successfulsignin=1
                    if len(cache['notification']):
                       notification('QlutaBot',cache['notification'])
                    bypass=0
                else:
                    notification('QlutaBot','Incorrect Credentials')
                    bypass=1
            else:
                bypass=0
            f=requests.get(settingskeystore['apiurl']+'api/getstat?'+str(settingskeystore['username'])+'?full',headers={'User-Agent': 'QluteClient-'+str(gamever)},timeout=5)
            f=json.loads(f.text)
            if bypass:
                issigned=0
            elif not f['restricted']:
                totrank=int(f['rank'])
                totperf=int(f['points'])
                totscore=int(f['score'])
                totacc=float(f['accuracy'])
                level=int(f['level'])
                issigned=1
            else:
                restricted=1
                issigned=0
                notification('QlutaBot',restrictedmsg)
        except Exception as err:
            print(err,time.time())
            totscore=0
            totperf=0
            totacc=0
            level=1
            totrank=0

def ondemand():
    global totperf,totscore,totrank,nettick,issigned,qlutaerror,menunotice,pingspeed,downloadqueue,level,multitime,multilist
    qlutaerror=True
    pingspeed=0
    while True:
        if stop:
            exit()
        if int(time.time()-nettick)>9:
            if not bypass_multiplayer:
                multilist=requests.get(settingskeystore['apiurl']+'api/getmultilist',headers={'User-Agent': 'QluteClient-'+str(gamever)},timeout=5).json()
            if issigned:
                try:
                    reloadprofile()
                    if activity==4:
                        pre='Playing '
                    else:
                        pre='Listening to '
                    ps=time.time()
                    f=requests.get(settingskeystore['apiurl']+'api/setstatus?'+str(settingskeystore['username'])+'?playing?'+str(pre+str(beattitle)),headers={'User-Agent': 'QluteClient-'+str(gamever)},timeout=5)
                    f=f.text
                    menunotice=requests.get(settingskeystore['apiurl']+'api/menunotice',headers={'User-Agent': 'QluteClient-'+str(gamever)},timeout=5).text
                    qlutaerror=False
                    pingspeed=int((time.time()-ps)/0.01)
                except Exception as err:
                    totperf=0
                    totscore=0
                    totacc=0
                    pingspeed=0
                    totrank=0
                    level=1
                    menunotice='Server is Busy'
                    try:
                        notification('Server Error',desc=str(err))
                    except Exception:
                        pass
                    qlutaerror=True
            nettick=time.time()
            for a in downloadqueue:
                try:
                    with requests.get(a[1],headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=3, stream=True) as r:
                        filename=r.headers['content-disposition']
                        filename = re.findall("filename=(.+)", filename)[0]
                        filename = unquote(filename).replace('"','')
                        block_size=4096
                        total_size = int(r.headers.get("content-length", 0))//block_size
                        tick=0
                        with open(downpath+filename+'.tmp','wb') as f:
                            for chunk in r.iter_content(chunk_size=block_size): 
                                tick+=1
                                a[2]=round(tick/total_size*100,2)
                                f.write(chunk)
                        os.rename(downpath+filename+'.tmp',downpath+filename)
                except Exception as err:
                    print(err)
                downloadqueue.remove(a)


        time.sleep(1/10)