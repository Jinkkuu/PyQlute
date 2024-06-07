room=[]
def multiplayer():
    global sysbutton,mu
    if activity in (14,15):
        render('rect', arg=((0,100,w,h-160), hcol[2], False))
    if activity==14:
        dq=[]
        dqu=[]
        if len(multilist):
            for a in multilist:
                playerlist=a['player_list'].replace(';',',')
                playercount=len(a['player_list'].split(';'))
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
        playerlist=room['player_list'].replace(';',',')
        players=room['player_list'].split(';')
        playercount=len(players)
        host=room['host']
        c=0
        render('rect', arg=((0,100,260,h-160), hcol[1], False)) # type: ignore
        for a in players: # type: ignore
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
        render('rect', arg=((w-400,(h//2)-80,410,100), blend(opacity,50), False),borderradius=10) # type: ignore
        render('text', text=room['currently_playing'], arg=((w-380,(h//2)-60), forepallete))
    if activity in (14,15):
        render('rect', arg=((0,0,w,100), hcol[0], False))
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        ta=[(-10,h-60,100,60),]
        te=['Back',]
        if activity==15:
            pass
        elif activity==14:
            ta.append((w-100,h-60,100,60))
            te.append('Create')
        sysbutton=menu_draw(ta,te,bradius=0,styleid=3)
        render('text', text=title, arg=((20,20), forepallete,'grade'))