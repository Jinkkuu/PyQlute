room=[]
multitext=''
isplaying=0
def multiplayer():
    global sysbutton,mu,multitext,beat
    if activity in (14,15,16):
        render('rect', arg=((0,100,w,h-160), hcol[2], False))
    if activity==14:
        dq=[]
        dqu=[]
        if len(multilist):
            for a in multilist:
                player=a['player_list'].rstrip(';')
                playerlist=player.replace(';',',')
                playercount=len(player.split(';'))
                if playercount>4:
                    playerlist=''
                    for b in a['player_list'].split(';'):
                        playerlist+=b+','
                    playerlist=playerlist+'+'
                dqu.append(str(playercount)+' ('+str(playerlist)+')\n'+str(a['currently_playing'])+'\n'+str(a['room_name']))
            for a in range(1,len(multilist)+1):
                dq.append(((w//2)-300,shopscroll+110+(100*(a-1)),600,90))
        else:
            render('text', text='No rooms are avaliable o-o', arg=((0,0), forepallete,'center'),relative=(w//2,h//2,0,0))
        mu=menu_draw(dq,dqu,bradius=10,styleid=3,selected_button=sbid,newline='\n')
        title='Multiplayer'
    elif activity==15:
        title='Room'
        player=room['player_list']
        playerlist=player.replace(';',',')
        players=player.split(';')
        playercount=len(players)
        host=room['host']
        c=0
        render('rect', arg=((0,100,260,h-160), hcol[1], False)) # type: ignore
        for a in players: # type: ignore
            if a!='':
                if a==host: # type: ignore
                    col=222, 210, 131
                elif a==settingskeystore['username']: # type: ignore
                    col=166, 207, 255
                else:
                    col=forepallete # type: ignore
                leadpos=(20,(120)+(60*c),220,40) # type: ignore
                render('rect', arg=(leadpos, blend(opacity,50), False),borderradius=10) # type: ignore
                render('text', text=str(a[:10]), arg=((27,leadpos[1]+8), col)) # type: ignore
                #render('text', text=a['mods'], arg=((218-t,leadpos[1]+9), col,'min','rtl')) # type: ignore
                #render('text', text=format(int(a['score']),',')+' - '+str(int(a["points"]))+'pp ('+str(int(a['combo']))+'x) '+timeform(int(time.time()-a['time'])), arg=((17,leadpos[1]+30), col,'min')) # type: ignore
                c+=1
        if settingskeystore['username']==host:
            suf='Change map\n'
        else:
            suf='Waiting for host...\n'
        beat=menu_draw(((w//2-120,(h//2)-80,450,size*1.2),),(suf+str(room['currently_playing']),),styleid=3,newline='\n')

    elif activity==16:
        title='Create Room'
        l=255,255,255
        if len(multitext)>=maxletters:
            multitext=multitext[:maxletters]
        render('text', text='Room Name:', arg=((w//2-300,h//2-80), forepallete))
        textbox((w//2-300,h//2-50,600),40,text=multitext,border_colour=l,center=True)
        beat=menu_draw(((w//2-(cardsize//2),h//2+(size//2),cardsize,size),),(songtitle,),styleid=3)
        #
    if activity in (14,15,16):
        render('rect', arg=((0,0,w,100), hcol[0], False))
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        ta=[(-10,h-60,100,60),]
        te=['Back',]
        if activity==15:
            pass
        elif activity in (14,16):
            ta.append((w-100,h-60,100,60))
            te.append('Create')
        sysbutton=menu_draw(ta,te,bradius=0,styleid=3)
        render('text', text=title, arg=((20,20), forepallete,'grade'))