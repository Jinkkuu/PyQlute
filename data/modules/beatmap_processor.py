from data.modules.bootstrap import getuserdata,gamepath,getscreen
from data.modules.audio import load_music,reset_tick
import os,time,json,pygame
from random import choice
reload_database = 1
beatmaplist={}
beatmapselect=[]
steps='artist','title','beatmapsetid','creator'
template='[General]','[Editor]','[Metadata]','[Difficulty]','[Events]','[TimingPoints]','[HitObjects]'
perfbom=0.075
background=pygame.surface.Surface((0,0))
objects=None
keycount=4
pos=[]
enable_experimental=0
def getpoint(perfect,good,meh,bad,multiplier,combo=1,type=int): # Points System 2024/06/15
    multiplier=multiplier
    if bad==0:
        bad+=1
    tmp=((perfect)+(good/2)+(meh/3))/bad
    tmp*=perfbom*multiplier
    return type(tmp)
def loadstats(file,find=0):
    print(file)
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
    global beatmaplist,beatmapselect
    difficulties=[]
    pointlist=[]
    tmp=[]
    lengths=[]
    diffs=[]
    beatmapids=[]
    for b in os.listdir(gamepath+value):
        if b.endswith('.osu'):
            cache=loadstats(gamepath+value+'/'+b)
            try:
                lengths.append(int(cache['hitobjects'][-1][2]))
            except Exception as err:
                print(err)
                lengths.append(0)
            if "version" in cache['metadata']:
                version=cache['metadata']['version']
            else:
                version='Untitled'
            if "beatmapid" in cache['metadata']:
                beatmapids.append(cache['metadata']['beatmapid'])
            else:
                beatmapids.append(None)
            tmp.append((version,getpoint(len(cache['hitobjects']),0,0,0,1,len(cache['hitobjects']),float),b))
    tmp=sorted(tmp, key=lambda x: x[1])
    for b in tmp:
        difficulties.append(b[0])
        pointlist.append(b[1])
        diffs.append(b[2])
    try:
        songtitle=value[value.index(' '):]
    except Exception:
        songtitle=value
    try:
        bpm=float(cache['timingpoints'][0][1])
    except Exception:
        bpm=0
    if bpm>0:
        bpm=60000/bpm
    if "audiofilename" in cache['general']:
        audiofile=cache['general']['audiofilename']
        if audiofile[0] == ' ':
            audiofile=audiofile[1:]
    else:
        audiofile=None
    beatmaplist[songtitle]={'raw':value,'songtitle':songtitle,'audiofile':audiofile,'maps':difficulties,'diffurl':diffs,'points':pointlist,'beatmapids':beatmapids,'bpm':int(bpm),'lengths':lengths}
    print(songtitle)
    id=0
    for c in steps:
        try:
            beatmaplist[songtitle][c]=cache['metadata'][c]
        except KeyError as err:
            if c == 'beatmapsetid':
                beatmaplist[songtitle][c]=0
            #print(id,err)
        id+=1
    if save:
        w=open(getuserdata()+'beatmaps.json','w')
        w.write(json.dumps(beatmaplist))
        w.close()
        beatmapselect=list(beatmaplist.values())
def reloadbeatmaps():
    global beatmaplist,beatmapselect
    if not os.path.isfile(getuserdata()+'beatmaps.json'):
        beatmaplist={}
        beatmapselect=[]
        for a in sorted(os.listdir(gamepath), key=get_creation_time):
            if not a.endswith('.tmp'):
                addbeatmap(a)
        beatmapselect=list(beatmaplist.values())
        w=open(getuserdata()+'beatmaps.json','w')
        w.write(json.dumps(beatmaplist))
        w.close()
    else:
        try:
            uhohmusic=0
            print('Loading beatmaps database...')
            beatmaplist=json.loads(open(getuserdata()+'beatmaps.json','r').read())
            gamecheck=[]
            for a in os.listdir(gamepath):
                if not a.endswith('.tmp'):
                    gamecheck.append(a)
            if len(beatmaplist):
                for a in beatmaplist:
                    if not beatmaplist[a]['raw'] in gamecheck and not str(beatmaplist[a]['raw']).endswith('.tmp'):
                        uhohmusic=1
                        break
            else:
                uhohmusic=1
            if uhohmusic:
                print('Uh-Oh!, All my music has disappeared!! >n<\nReloading your beatmaps, might take a while')
                os.remove(getuserdata()+'beatmaps.json')
                reloadbeatmaps()
            beatmapselect=list(beatmaplist.values())
        except Exception as err:
            print('Uh-Oh!, Your database for your beatmaps has been corrupted >n<\nReloading your beatmaps, might take a while\n'+str(err))
            os.remove(getuserdata()+'beatmaps.json')
            reloadbeatmaps()
reloadbeatmaps()
def random_beatmap():
    global songcache
    songcache = choice(list(beatmaplist.values()))
    return songcache
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

def grabobjects(value):
    global objects,pos
    try:
        objects=loadstats(value)['hitobjects']
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
        print(err)
        pos=None
        setkeycount(4)
        objects=None
def getobjects():
    return objects
oldw=0
oldh=0
bg=pygame.surface.Surface((0,0))
def getbackground(w,h):
    global oldw,oldh,bg
    if oldw != w or oldh != h or bg:
        oldw=w
        oldh=h
        bg = pygame.transform.scale(background,(w+10,h+10))
    else:
        bg=0
    return bg
def reloadbg(value,base):
    global background,bump,sc,bg
    try:
        x=loadstats(value)['events']
        x=x[1]
        if len(x)>4:
            backgroundev=x[2].rstrip('"')[1:]
            w,h= getscreen()
            b=0.50
            background=pygame.image.load(base+backgroundev).convert()
            bg=background
            #background.fill((255*b, 255*b, 255*b,128), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            background=0
        
    except Exception as err:
        print(err)
        background=0
rankmodes=('Ranked',(100,200,100)),('Unranked',(200,100,100)),('Special',(200,200,100)),('Loading...',(200,200,200)),