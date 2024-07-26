from data.modules.bootstrap import getuserdata,gamepath,getscreen
from data.modules.audio import load_music,reset_tick
import os,time,json,pygame,sqlite3
from random import choice
reload_database = 1
beatmaplist={}
steps='artist','title','beatmapsetid','creator'
template='[General]','[Editor]','[Metadata]','[Difficulty]','[Events]','[TimingPoints]','[HitObjects]'
perfbom=0.075
background=pygame.surface.Surface((0,0))
objects=None
keycount=4
pos=[]
enable_experimental=0
oldnames='beatmaps.json','beatmaps.db'
def getpoint(perfect,good,meh,bad,multiplier,combo=1,type=int): # Points System 2024/06/15
    multiplier=multiplier
    if bad==0:
        bad+=1
    tmp=((perfect)+(good/2)+(meh/3))/bad
    tmp*=perfbom*multiplier
    return type(tmp)
def loadstats(file,find=0):
    map=open(file,encoding='utf-8',errors='replace').read().split('\n')
    cache={}
    for a in template:
        try:
            title=a.strip('[').rstrip(']').lower()
            if not title in ('hitobjects','timingpoints','events'):
                cache[title]={}
            else:
                cache[title]=[]
            cac=map[map.index(a)+1:]
            cac=cac[:cac.index('')]
        
            count=0
            for b in cac:
                if not title in ('hitobjects','timingpoints','events'):
                    t=b.split(':')
                    if len(t)>1:
                        cache[title][t[0].lower()]=t[1]
                else:
                    t=b.split(',')
                    cache[title].append(t)
                count+=1
        except ValueError:
            pass
    return cache
def get_creation_time(item):
    item_path = os.path.join(gamepath, item)
    return os.path.getctime(item_path)
def addbeatmap(value,save=False):
    global beatmaplist
    difficulties=[]
    starratings=[]
    tmp=[]
    lengths=[]
    diffs=[]
    beatmapids=[]
    for b in os.listdir(gamepath+value):
        if b.endswith('.osu'):
            cache=loadstats(gamepath+value+'/'+b)
            hits=cache['hitobjects']
            try:
                lengths.append(int(hits[-1][2]))
            except Exception as err:
                print(err)
                lengths.append(0)
            if "version" in cache['metadata']:
                version=cache['metadata']['version']
            else:
                version='Untitled'
            if "beatmapid" in cache['metadata']:
                beatmapid=cache['metadata']['beatmapid']
            else:
                beatmapid=None
            #exit()
            tmp.append((version,suna(hits,float(cache['timingpoints'][0][1])),b,beatmapid))
    tmp=sorted(tmp, key=lambda x: x[1])
    beatmapids=[]
    for b in tmp:
        difficulties.append(b[0])
        starratings.append(b[1])
        diffs.append(b[2])
        beatmapids.append(b[3])
    try:
        songtitle=value[value.index(' '):]
    except Exception:
        songtitle=value
    try:
        bpm=float(cache['timingpoints'][0][1])
    except Exception:
        bpm=0
    if "audiofilename" in cache['general']:
        audiofile=cache['general']['audiofilename']
        if audiofile[0] == ' ':
            audiofile=audiofile[1:]
    else:
        audiofile=None
    metadata={}
    metadata['raw'] = value
    metadata['songtitle'] = songtitle
    metadata['audiofile'] = audiofile
    metadata['maps'] = str(difficulties)
    metadata['diffurl'] = str(diffs)
    metadata['starratings'] = str(starratings)
    metadata['beatmapids'] = str(beatmapids)
    metadata['bpm'] = int(bpm)
    metadata['lengths'] = str(lengths)
    print(songtitle)
    id=0
    for c in steps:
        try:
            metadata[c]=cache['metadata'][c]
        except KeyError as err:
            if c == 'beatmapsetid':
                metadata[c]=0
        id+=1
    beatmaplocalapi.execute("INSERT INTO beatmaps (raw,artist,title,creator,beatmapsetid,songtitle,audiofile,maps,diffurl,starratings,beatmapids,bpm,lengths) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(metadata['raw'],metadata['artist'],metadata['title'],metadata['creator'],metadata['beatmapsetid'],metadata['songtitle'],metadata['audiofile'],metadata['maps'],metadata['diffurl'],metadata['starratings'],metadata['beatmapids'],metadata['bpm'],metadata['lengths']))
    if save:
        beatmaps.commit()
        beatmaplist=beatmaplocalapi.execute("SELECT * FROM beatmaps;").fetchall()
def reloadbeatmaps():
    global beatmaplist,beatmaps,beatmaplocalapi
    beatmaps = sqlite3.connect(getuserdata()+'qlute.db')
    beatmaps.row_factory = sqlite3.Row
    beatmaplocalapi = beatmaps.cursor()
    for a in oldnames:
        if os.path.isfile(getuserdata()+a):
            os.remove(getuserdata()+a)
    if not beatmaplocalapi.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='beatmaps';").fetchone():
        beatmaplocalapi.execute("CREATE TABLE beatmaps(raw,artist,title,creator,beatmapsetid INT,songtitle,audiofile,maps,diffurl,starratings,beatmapids,bpm INT,lengths)")
        for a in sorted(os.listdir(gamepath), key=get_creation_time):
            if not a.endswith('.tmp'):
                addbeatmap(a)
        beatmaps.commit()
        beatmaplist=beatmaplocalapi.execute("SELECT * FROM beatmaps;").fetchall()
    else:
        try:
            uhohmusic=0
            print('Loading beatmaps database...')
            beatmaplist=beatmaplocalapi.execute("SELECT * FROM beatmaps;").fetchall()
            gamecheck=[]
            for a in os.listdir(gamepath):
                if not a.endswith('.tmp'):
                    gamecheck.append(a)
            if len(beatmaplist):
                for a in range(0,len(beatmaplist)):
                    if not beatmaplist[a]['raw'] in gamecheck and not str(beatmaplist[a]['raw']).endswith('.tmp'):
                        print('err',beatmaplist[a]['raw'])
                        uhohmusic=1
                        break
            else:
                uhohmusic=1
            if uhohmusic:
                print('Uh-Oh!, All my music has disappeared!! >n<\nReloading your beatmaps, might take a while')
                beatmaplocalapi.execute('DROP TABLE beatmaps')
                reloadbeatmaps()
        except Exception as err:
            print('Uh-Oh!, Your database for your beatmaps has been corrupted >n<\nReloading your beatmaps, might take a while\n'+str(err))
            beatmaplocalapi.execute('DROP TABLE beatmaps')
            reloadbeatmaps()
def random_beatmap():
    global songcache
    from random import randint
    songcache = beatmaplist[randint(1,len(beatmaplist))-1]
    return songcache,beatmaplist.index(songcache)
def get_info(value):
    try:
        return songcache[value]
    except Exception:
        return None
def beatmap_count():
    return len(beatmaplist)
def cache_beatmap(value):
    global songcache,background
    reset_tick()
    songcache=beatmaplist[value]
def getkeycount():
    return keycount
def getkeypos():
    return pos
def setkeycount(val):
    global keycount
    keycount=val
def gettiming():
    return timings
def grabobjects(value):
    global objects,pos,timings
    try:
        before = loadstats(value)
        timings=[(a[0],a[-1]) for a in before['timingpoints']]
        objects=before['hitobjects']
        x=[]
        for a in objects:
            key=a[0]
            if not key in x:
                x.append(key)
        keycount=len(x)
        if keycount>7 or not enable_experimental:
            keycount=4
        setkeycount(keycount)
        pos=x[:keycount]
    except Exception as err:
        print(err,'go function')
        pos=None
        setkeycount(4)
        objects=None
def suna(ob,bpm):
    starrating=0
    if ob:
        x=0
        for a in ob:
            so=int(a[2])
            if so>x:
                suna=((so-x)/bpm)
                if not suna<1.1:
                    suna=0
                #print('[S U N A]',round(suna,2),str(round(starrating,2))+' Stars ')
                starrating+=suna*0.01
                x=so
    return starrating
def getobjects():
    return objects
oldw=0
oldh=0
bg=pygame.surface.Surface((0,0))
def getbackground(w,h):
    global oldw,oldh,bg
    try:
        if oldw != w or oldh != h and background:
            oldw=w
            oldh=h
            bg = pygame.transform.smoothscale(background,(w+10,h+10))
        elif not background:
            bg=0
    except TypeError:
        bg=0
    return bg
def reloadbg(value,base):
    global background,bump,sc,bg,oldw,oldh
    try:
        x=loadstats(value)['events']
        x=x[1]
        if len(x)>4:
            backgroundev=x[2].rstrip('"')[1:]
            w,h= getscreen()
            b=0.50
            oldw, oldh=0, 0
            background=pygame.image.load(base+backgroundev).convert()
            bg=background
        else:
            background=0
        
    except Exception as err:
        print(err)
        background=0
rankmodes=('Ranked',(100,200,100)),('Unranked',(200,100,100)),('Special',(200,200,100)),('Loading...',(200,200,200)),
reloadbeatmaps()