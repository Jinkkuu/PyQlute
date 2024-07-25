import requests,time,json,re,os
from urllib.parse import unquote
from data.modules.bootstrap import getstop,version,notification,downpath
from data.modules.settings import getsetting
from data.modules.beatmap_processor import get_info
from pypresence import Presence

client_id = '1251396255381327966'  # Client ID
RPC = Presence(client_id)  # Initialize the client class
issubmiting = 0
successfulsignin=0
totrank=0
totperf=0
totscore=0
totacc=0
level=0
prevrank=0
oldstats=[totperf,totscore,totacc,level]
leaderboard=[]
menunotice=''
ranktype=1
restricted=0
restrictedmsg='Your account has been restricted, You are not able to use any online features at this state'
downloadqueue=[]
issigned=0
def getnotice():
    return menunotice
def getsigned():
    return issigned
def togsign():
    global issigned
    issigned=not issigned
def rsus():
    global successfulsignin
    successfulsignin=0
def getmystats():
    return totacc,totperf,totrank,totscore,level
def getsubmitstatus():
    return issubmiting
def getoldstat():
    return oldstats
def setsubmit(val):
    global issubmiting
    issubmiting=val
def submit_score(perf,combo,beatmapid,beatmapsetid,max,great,meh,bad,difficulty,mods,maxperf,taken):
    global oldstats,issubmiting,prevrank
    prevrank=totrank
    oldstats=[totperf,totscore,totacc,level]
    print('Submitting Score...')
    template=get_info('songtitle')+';'+str(perf)+';'+str(combo)+';'+str(beatmapid)+';'+str(beatmapsetid)+';'+str(max)+';'+str(great)+';'+str(meh)+';'+str(bad)+';'+str(difficulty)+';'+str(mods)+';'+str(maxperf)+';'+str(taken) # type: ignore
    f=requests.get(getsetting('apiurl')+'api/submitscore?'+str(getsetting('username'))+';'+str(getsetting('password'))+';'+str(template),headers={'User-Agent': 'Qlutev3Client-'+version()[0]},timeout=10) # type: ignore
    f=f.text
    reloadprofile() # type: ignore
    issubmiting = 0
    if f!='':
        print(f.rstrip('\n'))
        notification('QlutaBot',desc=f.rstrip('\n')) # type: ignore
def reloadprofile():
    global totperf,totscore,totrank,totacc,issigned,successfulsignin,restricted,level,qlutaerror
    if getsetting('username')!='':
        try:
            if not successfulsignin:
                f=requests.get(getsetting('apiurl')+'api/chkprofile?'+str(getsetting('username'))+'?'+str(getsetting('password')),headers={'User-Agent': 'Qlutev3Client-'+version()[0]},timeout=5)
                cache=json.loads(f.text)
                if int(cache['success'])==1:
                    if len(cache['notification']):
                       notification('QlutaBot',cache['notification'])
                    bypass=0
                    successfulsignin=1

                else:
                    notification('QlutaBot','Incorrect Credentials')
                    print('Incorrect Creds')
                    bypass=1
            else:
                bypass=0
            f=requests.get(getsetting('apiurl')+'api/getstat?'+str(getsetting('username'))+'?full',headers={'User-Agent': 'Qlutev3Client-'+version()[0]},timeout=5)
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
def getleaderboard():
    return leaderboard
def rleaderboard(value):
    global leaderboard
    leaderboard=[]
    try:
        f=requests.get(getsetting('apiurl')+'api/getleaderboard?'+str(value))
        leaderboard=f.json()
    except Exception:
        pass
def ondemand():
    global totperf,totscore,totrank,nettick,issigned,qlutaerror,menunotice,pingspeed,downloadqueue,level,multitime
    from data.modules.bootstrap import getactivity
    qlutaerror=True
    pingspeed=0
    discordactive=0
    nettick=0
    if getsetting('username') and getsetting('password'):
        issigned=1
    while True:
        if getstop():
            exit()
        if int(time.time()-nettick)>9:
            if getactivity()==5:
                pre='Playing '
            else:
                pre='Listening to '
            status=pre+str(get_info('songtitle'))
#            if not bypass_multiplayer:
#                reloadrooms()
            if issigned:
                try:
                    ps=time.time()
                    f=requests.get(getsetting('apiurl')+'api/setstatus?'+str(getsetting('username'))+'?playing?'+str(status),headers={'User-Agent': 'Qlutev3Client-'+version()[0]},timeout=5)
                    f=f.text
                    menunotice=requests.get(getsetting('apiurl')+'api/menunotice',headers={'User-Agent': 'Qlutev3Client-'+version()[0]},timeout=5).text
                    qlutaerror=False
                    reloadprofile()
                except Exception as err:
                    print(err)
                    totperf=0
                    totscore=0
                    totacc=0
                    totrank=0
                    level=1
                    menunotice='Server is Busy'
#                    try:
#                        notification('Server Error',desc=str(err))
#                    except Exception:
#                        pass
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
                    print(err,'DOWNLOAD SEQUENCE')
                downloadqueue.remove(a)
            try:
                if getsetting('discordrpc'):
                    if not discordactive:
                        RPC.connect()
                        discordactive=1
                    if issigned:
                        user=getsetting('username')
                        rank=totrank
                        userstat=user+' (#'+format(rank,',')+')'
                    else:
                        rank=0
                        user='Guest'
                        userstat=user
                    RPC.update(state=status,large_image='main-image',large_text=userstat)
            except Exception as err:
                discordactive=0
                print(err)
        time.sleep(1/10)
def downloadmap(url,name='Unknown'):
    global downloadqueue
    downloadqueue.append([name,url,'Queued'])
def getqueue():
    return downloadqueue
def getstat(beatmapsetid):
    global ranktype
    from data.modules.shopscreen import beatmapapi,getrank
    ranktype=getrank(1)
    return 0
    x=1
    success=0
    block=0
    ranktype=3
    while x<4 and not success and time.time()-block>0:
        try:
            tmp=''
            with requests.get(beatmapapi+'s/'+str(beatmapsetid),headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=3, stream=True) as f:
                if f.status_code != 429:
                    tmp+=f.text
                    error=0
                else:
                    error=1
            if not error:
                f=json.loads(tmp)
                f=f['RankedStatus']
                ranktypetmp=int(f)
            else:
                ranktypetmp=-99
                block=time.time()+120
                print('You have been rate limited!! Slow down after 2 minutes~ >n<')
            success=1
        except Exception as error:
            print(error,'(Returning as Unranked)')
            x+=1
            ranktypetmp=1
    ranktype=getrank(ranktypetmp)