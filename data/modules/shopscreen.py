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
progress=0
srank=0
maxsentry=10
search=['','']
def reload_background():
    global bgs
    bgs=pygame.Surface((0,0))
    bgst=requests.get(sentry[sbid-1]['covers']['card'],headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=3)
    bgst=bgst.content
    bgst=io.BytesIO(bgst)
    bgst=pygame.image.load(bgst).convert_alpha()
    bgs=pygame.transform.scale(bgst, (350,180))

def shop_refresh(usecached):
    global sbt,sentrynf,sref,serr,sentry,progress
    serr=0
    try:
        if not usecached:
            sref=1
            if search[0]!='':
                alt='?query='+str(search[0])
            else:
                alt=''
            sentrynf=[]
            tick=0
            for progress in range(0,maxsentry+1): 
                try:
                    f = requests.get(beatmapapi+'search'+alt+'?limit=10&offset='+str(progress*10),headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=3)
                    f=f.json()['found']
                    for a in f:
                        if a['beatmaps'][0]['mode']=='mania':
                           sentrynf.append(a)
                except Exception as err:
                    print(err)
        sentry=[]
        tmp=[]
        for a in sentrynf:
            if getrank(a['ranked'])==srank:
                sentry.append(a)
                tmp.append(a['artist']+' - '+a['title'])
        sbt=tmp
        sref=0
    except Exception as err:
        print(err,'> Store')
        serr=1
def downloads():
    global sysbutton,dq,dqs,serr
    if activity==12:
        dq=[]
        dqu=[]
        for a in downloadqueue:
            dqu.append('Downloading - '+str(a[0]))
        render('rect', arg=((0,100,w,h-160), hcol[2], False))
        for a in range(1,len(downloadqueue)+1):
            dq.append(((w//2)-200,shopscroll+100+(80*(a-1)),400,80))
        dqs=menu_draw(dq,dqu,bradius=0,styleid=3,selected_button=sbid)
        render('rect', arg=((0,0,w,100), hcol[0], False))
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        render('text', text='Downloads', arg=((20,20), forepallete,'grade'))
        sysbutton=menu_draw(((-10,h-60,100,60),),('Back',),bradius=0,styleid=3)

def shopdirect():
    global activity,shopref,sysbutton,shopbutton,serr,shopbutton2,usecache
    if activity==6:
        if shopref or serr:
            threading.Thread(target=shop_refresh, args=(usecache,)).start()
            shopref=0
            usecache=0
            serr=0
        render('rect', arg=((0,100,w,h-160), hcol[2], False))
        sb=[]
        for a in range(1,len(sbt)+1):
            sb.append((400*((w/800)-1),shopscroll+120+(80*(a-1)),400,80))
        shopbutton=menu_draw((sb),(sbt),bradius=0,styleid=3,selected_button=sbid)
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        render('rect', arg=((0,0,w,100), hcol[0], False))
        render('rect', arg=((0,100,w-400,20), hcol[1], False))
        render('rect', arg=((w-400,100,400,h-160), hcol[1], False))
        render('text', text='Browse', arg=((20,20), forepallete,'grade'))
        textbox((0,80,300),20,text=search[0],center=True,min=True,bg_colour=hcol[0])
        shopbutton2=menu_draw(((0,100,100,20),(300,80,100,20),(100,100,100,20),(200,100,100,20),(300,100,100,20),), ('Refresh','Search','Ranked','Unranked','Special'),settings=True,selected_button=srank+3)
        if sref:
            loading.update()
            render('rect', arg=((25+(loading.value*(w-485)),h//2-25,40,40), forepallete, False),borderradius=int(40-(loading.value*25)))
            render('rect', arg=((27+(loading.value*(w-485)),h//2-22,35,35), (0,0,0), False),borderradius=int(35-(loading.value*25)))
            if progress:
                te=str(int((progress/maxsentry)*100))+'%'
            else:
                te='Loading...'
            render('text', text=te, arg=((20,20), forepallete,'grade','center'),relative=(400*((w/800)-1),100,400,h-100))
        if len(sb):
            try:
                t=-20
                t+=(-shopscroll/-(80*(len(sbt)-1)))*((h-180)-((h-180)//len(sb)))
                render('rect', arg=((0,120,10,h-180), (80,80,80), False))
                render('rect', arg=((0,100-t,10,(h-180)//len(sb)), hcol[0], False))
            except Exception:
                pass
        if sbid:
            crok=0
            entry=sentry[sbid-1]
            rank=getrank(entry['ranked'])
            render('rect', arg=((w-400+25,120,350,180), hcol[0], False))
            screen.blit(bgs,(w-400+25,120))
            render('text', text=entry['title'], arg=((w-400+25,335), forepallete))
            render('text', text=entry['artist'], arg=((w-400+25,360), forepallete))
            #render('text', text=entry['creator'], arg=((w-400+25,360), forepallete))
            render('text', text='BPM:'+str(entry['bpm'])+' - '+str(getpoint(entry['beatmaps'][0]['max_combo'],0,0,0,1,combo=entry['beatmaps'][0]['max_combo']))+'pp - '+clockify(entry['beatmaps'][0]['total_length']), arg=((w-400+25,310), forepallete))
            render('rect', arg=((w-400+30,250,100,40), rankmodes[rank][1], False),borderradius=10) # type: ignore
            render('text', text=rankmodes[rank][0], arg=((0,0), forepallete,'center'),relative=(w-400+30,250,100,40))
            print_card(0,0,entry['creator'],(w-400+25,390),0,hide=True) # type: ignore
        else:
            crok=999
        if sbid and entry['beatmaps'][0]['mode']!='mania':
            crok=999
            render('text', text='Beatmap not supported on '+gamename, arg=((w-400+25,480), forepallete))

        sysbutton=menu_draw(((-10,h-60,100,60),(w-140,crok+h-60,140,60)),('Back','Download'),bradius=0,styleid=3)