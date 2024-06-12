def get_input():
    global keys,logintext,textboxid,bgs,ismulti,multitext,reloaddatabase,room,debugmode,meidt,cset,activity,shopscroll,search,shopref,usecache,srank,modsv,sb,sbt,modsani,sbid,notewidth,noteheight,customid,successfulsignin,issigned,modshow,setupid,gobutton,useroverlay,replaymen,beatnowmusic,beatsel,beatsel,diffani,diffcon,beatnowmusic,change,setbutton,settingskeystore,fpsmode,firstcom,accounts
    for event in pygame.event.get():
        if event.type  ==  pygame.QUIT:
            transitionprep(-1)
        if event.type  ==  pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mixer.Sound(samplepath+'click.wav').play()
            if activity==1:
                if menubutton  ==  1:
                    if meid or bypass_multiplayer:
                        transitionprep(3)
                    else:
                        bani.start()
                        meidt=not meid
                elif menubutton  ==  2:
                    if not meid:
                        transitionprep(9)
                    else:
                        if issigned:
                            transitionprep(14)
                            sbid=0
                            ismulti=1
                        else:
                            transitionprep(10)
                elif menubutton  ==  3:
                    if not meid:
                        transitionprep(6)
                        shopscroll=0
                        sbid=0
                    else:
                        bani.start()
                        meidt=not meid
                elif menubutton  ==  4:
                    if not meid:
                        transitionprep(-1)
                elif topbutton  ==  1:
                    transitionprep(2)
                    setupid=1
                    customid=0
                elif topbutton  ==  2:
                    transitionprep(10)
                elif topbutton  ==  3:
                    shopscroll=0
                    sbid=0
                    transitionprep(12)
            elif activity==0:
                transitionprep(1)
            elif activity==16:
                if sysbutton==1:
                    transitionprep(14)
                elif sysbutton==2:
                    requests.get(settingskeystore['apiurl']+'api/createroom?'+str(settingskeystore['username'])+'?'+str(settingskeystore['password'])+'?'+str(multitext)+'?'+str(beatmapsetid)+'?'+str(beatmapid)+'?'+str(songtitle),headers={'User-Agent': 'QluteClient-'+str(gamever)},timeout=5)
                    reloadrooms()
                    transitionprep(14)
                elif beat:
                    transitionprep(3)
            elif activity==14:
                if sysbutton==1:
                    transitionprep(1)
                elif sysbutton==2:
                    multitext=settingskeystore['username']+"'s lovely playroom"
                    transitionprep(16)
                elif sbid==mu:
                    notification('QlutaBot',desc='Joining Room...')
                    room=multilist[mu-1]
                    transitionprep(15)
                elif mu:
                    sbid=mu
            elif activity==15:
                if sysbutton:
                    transitionprep(14)
            elif activity==12:
                if sysbutton==1:
                    transitionprep(1)
                elif event.button==1 and dqs:
                    sbid=dqs
                elif event.button==4:
                    if not shopscroll+20>0:
                        shopscroll+=40
                elif event.button==5:
                    if not shopscroll-20<-(80*(len(dq)-1)):
                        shopscroll-=40

            elif activity==6:
                if sysbutton==1:
                    
                    transitionprep(1)
                elif sysbutton==2:
                    notification('Downloading',desc=sentry[sbid-1]['artist']+' - '+str(sentry[sbid-1]['title']))
                    downloadqueue.append([sentry[sbid-1]['artist']+' - '+str(sentry[sbid-1]['title']),'https://catboy.best/d/'+str(sentry[sbid-1]['beatmaps'][0]['beatmapset_id']),'Queued'])
                elif event.button==1:
                    if shopbutton2 in (1,2):
                        if not sref:
                            shopref=1
                            sb=[]
                            sbt=[]
                    elif shopbutton2>2:
                        if srank!=shopbutton2-3:
                            if not sref:
                                srank=shopbutton2-3
                                usecache=1
                                sbid=0
                                shopref=1
                                shopscroll=0
                    elif shopbutton:
                        sbid=shopbutton
                        threading.Thread(target=reload_background).start()
                elif event.button==4:
                    if not shopscroll+20>0:
                        shopscroll+=40
                elif event.button==5:
                    if not shopscroll-20<-(80*(len(sbt)-1)):
                        shopscroll-=40
            elif activity==9:
                if sysbutton:
                    transitionprep(1)
            elif activity==11:
                if sysbutton:
                    transitionprep(2)
                elif event.button==1 and skinbutton:
                    sbid=skinbutton
                    settingskeystore['skin']=skins[sbid-1]
                    reloadsettings()
                    reloadicons()
                elif event.button==4:
                    if not shopscroll+20>0:
                        shopscroll+=40
                elif event.button==5:
                    if not shopscroll-20<-(80*(len(skins)-1)):
                        shopscroll-=40
            elif activity==10:
                if pygame.Rect(w//2-300,h//2-50,600,30).collidepoint(pygame.mouse.get_pos()):
                    textboxid=0
                elif pygame.Rect(w//2-300,h//2+30,600,30).collidepoint(pygame.mouse.get_pos()):
                    textboxid=1
                if logbutton==1:
                        if issigned:
                            settingskeystore['username']=None
                            settingskeystore['password']=None
                            logintext[1]=''
                            issigned=0
                            successfulsignin=0
                            notification('QlutaBot',desc='You are offline')
                        else:
                            if logintext[0]!='' or logintext[1]!='':
                                settingskeystore['username']=logintext[0]
                                settingskeystore['password']=hashlib.sha256(bytes(logintext[1],'utf-8')).hexdigest()
                            else:
                                notification('Qluta',desc='what u doin >:^')
                        threading.Thread(target=reloadprofile).start()
                        change=True
                elif logbutton==2:
                    if sys.platform=='win32':
                        os.startfile(settingskeystore['apiurl']+'signup')
                    elif sys.platform=='darwin':
                        os.system('open '+settingskeystore['apiurl']+'signup')
                    else:
                        try:
                            os.system('xdg-open '+settingskeystore['apiurl']+'signup')
                        except OSError:
                            pass

                if sysbutton:
                    transitionprep(1)
            elif activity==5:
                if butt:
                    if replaymen:
                        transitionprep(6)
                        replaymen=not replaymen
                    else:
                        transitionprep(3)
            elif activity==2:
                if catbutton and not catbutton==2:
                    setupid=catbutton
                elif catbutton==2:
                    transitionprep(11)
                    sbid=skinid
                    shopscroll=0
                if setbutton:
                    change=True
                if setbutton  ==  1 and setupid==4:
                    change=True
                    if fpsmode<1:
                        fpsmode=len(fpsmodes)-1
                    else:
                        fpsmode-=1
                    settingskeystore['fps']=fpsmodes[fpsmode]
                elif setbutton == 3 and setupid==1:
                    change=True
                    settingskeystore['sreplay']=not settingskeystore['sreplay']
                elif setbutton == 6 and setupid==1:
                    change=True
                    settingskeystore['fpsmetre']=not settingskeystore['fpsmetre']
                elif setbutton == 2 and setupid==4:
                  settingskeystore['fullscreen'] = not settingskeystore['fullscreen']
                  firstcom=False
                elif setbutton == 1 and setupid==3:
                  settingskeystore['hitsound'] = not settingskeystore['hitsound']
                elif setbutton == 1 and setupid==1:
                  settingskeystore['leaderboard'] = not settingskeystore['leaderboard']
                elif setbutton == 2 and setupid==1:
                  settingskeystore['effects'] = not settingskeystore['effects']
                elif setbutton == 4 and setupid==1:
                  settingskeystore['bgmm'] = not settingskeystore['bgmm']
                elif setbutton == 5 and setupid==1:
                    transitionprep(13)
                    cset=-1
                elif sysbutton:
                    transitionprep(1)
            elif activity==13:
                if sysbutton==1:
                    transitionprep(1)
                elif sysbutton:
                    cset=sysbutton-1
            elif activity==3 or activity==7:
                if event.button==1:
                    if sysbutton  ==  1:
                        if not activity==7:
                            if ismulti:
                                transitionprep(16)
                            else:
                                transitionprep(1)
                        else:
                            activity=3
                    elif sysbutton == 2:
                        modshow=not modshow
                        modsani=[Tween(begin=modsv, end=1,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),modshow]
                        modsv=modsani[0].value
                        modsani[0].start()
                    else:
                        if gobutton:        
                            if not activity==7:
                                if len(diff)>1:
                                    activity=7
                                else:
                                    preparemap()
                            else:
                                preparemap()
                        else:
                            if mod:
                                for a in range(1,len(modsen)+1):
                                    if mod==a:
                                        modsen[a-1]=not modsen[a-1]
                                        reloadstats()
                            else:
                                if button:
                                    if activity!=7:
                                        if button-1!=beatsel:
                                            beatnowmusic=1
                                            beatsel=button-1
                                            diffcon=0
                                        else:
                                            if not activity==7:
                                                if len(diff)>1:
                                                    activity=7
                                                else:
                                                    preparemap()
                                            else:
                                                preparemap()
                                    else:
                                        if button-1!=diffcon:
                                            diffcon=button-1
                                            diffani=[Tween(begin=cross[1], end=diffcon,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
                                            diffani[0].start()
                                            reloadstats()
                                        else:
                                            preparemap()
                elif event.button==4:
                        if not activity==7:
                            if cross[0]!=0:
                                cross[0]-=1
                        else:
                            if cross[1]!=0:
                                cross[1]-=1
                elif event.button==5:
                        if not activity==7:
                            if cross[0]!=len(p2)-1:
                                cross[0]+=1
                        else:
                            if cross[1]!=len(bp2)-1:
                                cross[1]+=1


        if event.type  ==  pygame.KEYDOWN:
            if event.key  ==  pygame.K_F5:
                debugmode=not debugmode
            if event.key  ==  pygame.K_F3:
                notification('Reloaded!',desc='Reloaded icons for you!')
                reloadicons()
            if event.key  ==  pygame.K_MINUS and not activity==10:
                volchg(0)
            elif event.key  ==  pygame.K_EQUALS and not activity==10:
                volchg(1)
            elif event.key  ==  pygame.K_F9 and not activity==10:
                useroverlay=not useroverlay
            elif event.key == pygame.K_BACKSPACE: 
                if activity==10:
                    logintext[textboxid] = logintext[textboxid][:-1]
                elif activity==6:
                    search[0] = search[0][:-1]
                elif activity==3:
                    tmp=search[1]
                    search[1] = search[1][:-1]
                    if len(search[1])!=len(tmp):
                        reload_database()
            elif event.key == pygame.K_TAB: 
                if activity==10:
                    textboxid=not textboxid
            elif event.key  ==  pygame.K_RETURN:
                if activity==10:
                    pass # Bypass repeated sequence
                elif activity==6:
                    shopref=1
                    sb=[]
                    sbt=[]

            # Unicode standard is used for string 
            # formation 
            elif event.key  ==  pygame.K_q and not activity==10 or event.key  ==  pygame.K_ESCAPE :
                if activity==4:
                    transitionprep(3)
                elif activity==1:
                    if meid:
                        bani.start()
                        meidt=not meid
                    else:
                        transitionprep(-1)           
                elif not activity==7:
                    if ismulti:
                        transitionprep(16)
                    else:
                        transitionprep(1)
                elif activity==7:
                    activity=3
            else: 
                if activity==10:
                    logintext[textboxid] += event.unicode
                elif activity==6:
                    search[0] += event.unicode
                elif activity==3:
                    tmp=search[1]
                    search[1] += event.unicode
                    if len(search[1])!=len(tmp):
                        reload_database()
            if activity==7 or activity==3:
                if event.key  ==  pygame.K_RETURN:
                    if len(p2):
                        if not activity==7:
                            if len(diff)>1:
                                activity=7
                            else:
                                preparemap()
                        else:
                            preparemap()
                if activity==3:
                    if event.key == pygame.K_END:
                        if len(fullbeatmapname)!=0:
                            beatsel=len(p2)-1
                            beatnowmusic=1
                    if event.key == pygame.K_HOME:
                        if len(fullbeatmapname)!=0:
                            beatsel=0
                            beatnowmusic=1
                    if event.key == pygame.K_F2:
                        if len(fullbeatmapname)!=0:
                            beatsel=random.randint(1,len(fullbeatmapname))-1
                            beatnowmusic=1
                if event.key  ==  pygame.K_UP:
                    if activity!=7:
                        song_change(0)
                    else:
                        diff_change(0)
                if event.key  ==  pygame.K_DOWN:
                    if activity!=7:
                        song_change(1)
                    else:
                        diff_change(1)
                        
                if event.key  ==  pygame.K_e:
                    change_diff()    
            elif activity==5:
                if event.key == pygame.K_q:
                    if replaymen:
                        transitionprep(6)
                        replaymen=not replaymen
                    else:
                        transitionprep(3)
            elif activity==13:
                settingskeystore['Key'+str(cset)]=event.unicode
                if cset!=4 and not cset<0:
                    cset+=1
                elif cset==4:
                    cset=-1
                    reloadsettings()
                    transitionprep(2)
            elif activity==4:
                for a in range(0,4):
                    if event.unicode  ==  settingskeystore['Key'+str(a+1)]:
                        keys[a]=1
                if event.key  ==  pygame.K_BACKQUOTE:
                    beatnowmusic=1
                    resetscore() # type: ignore
        if event.type  ==  pygame.KEYUP:
            if activity==4:
                if event.key  ==  pygame.K_t:
                    tip=0
                for a in range(0,4):
                    if event.unicode  ==  settingskeystore['Key'+str(a+1)]:
                        keys[a]=0