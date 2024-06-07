import pygame
modsalias="Auto",'Blind','Slice','EZ','Random'#,'DT','HT'
modsaliasab='AT','BD','SL','EZ','RND'#,'DT','HT'
mods=''
def reload_database():
    global reloaddatabase,cross,beatsel
    reloaddatabase=1
    if not fbt in fullbeatmapname and len(p2):
        song_change(1)
    cross[0]=0
def get_mods(bpos):
    global mods
    b=0
    tap=0
    mods=''
    for a in modsaliasab:
        if modsen[b]:
            pos=(bpos[0]+(15*tap),bpos[1])
            rec=icons['emblem.png'].get_rect() # type: ignore
            screen.blit(icons['emblem.png'],pos) # type: ignore
            mods+=a
            render('text', text=a, arg=((0,0), (0,0,0),'center'),relative=(pos[0],pos[1],rec[2],rec[3])) # type: ignore
            tap+=1
        b+=1
def beatmenu():
    global activity,beatsel,modsani,beatnowmusic,background,menuback,cross,diffcon,hits,modshow,mod,modsen,button,beatsel,speedvel,scoremult,msg,sysbutton,gobutton,go
    go=False
    if activity==3 or activity==7:
        modsani[0].update()
        if modsani[0].value==100 or not modshow:
            modsani[1]=0
        if beatani[0].value==beatsel: # type: ignore
            beatani[1]=1 # type: ignore
        else:
            beatani[0].update() # type: ignore
        if diffani[0].value==diffcon: # type: ignore
            diffani[1]=1 # type: ignore
        else:
            diffani[0].update() # type: ignore
        try:
            if background:
                screen.blit(background, (0,0)) # type: ignore
        except Exception:
            background=0
        if activity==3:
            idc=0
            idcb=len(p2)
        else:
            idc=1
            idcb=len(bp2)
        scrollbar((w-10,54),(10,h-118),search=-cross[idc],length=idcb)
        a=0
        tmp=(h//60)//2 # type: ignore
        if beatmaps>0: # type: ignore
            pp=int(int(getpoint(diffp[0][0],0,0,0,scoremult,combo=diffp[0][0]))),int(getpoint(diffp[-1][0],0,0,0,scoremult,combo=diffp[-1][0])) # type: ignore
            if len(diffp)<2 or activity==7: # type: ignore
                gotext='Q'
            else:
                gotext='->'
        if activity==7:
            sel=diffcon
            button=menu_draw(bp1,bp2,beatmenu=True,selected_button=sel+1,startlimit=int(cross[1])-tmp-1,endlimit=int(cross[1])+tmp+2,crossid=1,styleid=1) # type: ignore
        else:
            sel=beatsel
            button=menu_draw(p1,p2,beatmenu=True,selected_button=sel+1,startlimit=int(cross[0])-tmp-1,endlimit=int(cross[0])+tmp+2,crossid=0,styleid=1) # type: ignore
        if beatmaps==0: # type: ignore
            crok=999
        else:
            crok=0
        if restricted or not isquest: # type: ignore
            crub=999
        else:
            crub=0
        if pygame.Rect(0,(h//4),45,h//2).collidepoint(pygame.mouse.get_pos()): # type: ignore
            t=0
        else:
            t=225
        if 1==1: # Leaderboard idk why this is here lol
            s=310
            c=0
            if issigned: # type: ignore
                render('rect', arg=((220-t,(h//2)-(s//2),45,s), blend(opacity,25), False),borderradius=10) # type: ignore
                render('rect', arg=((-10-t,(h//2)-(s//2),250,s), blend(opacity,0), False),borderradius=10) # type: ignore
                for a in leaderboard[:5]: # type: ignore
                    if a['username']==settingskeystore['username']: # type: ignore
                        col=166, 207, 255
                    else:
                        col=forepallete # type: ignore
                    leadpos=(10-t,(10+((h//2)-(s//2)))+(60*c),220,50) # type: ignore
                    render('rect', arg=(leadpos, blend(opacity,50), False),borderradius=10) # type: ignore
                    render('text', text=str('#'+str(c+1)+' '+a["username"][:10]), arg=((17-t,leadpos[1]+5), col)) # type: ignore
                    render('text', text=a['mods'], arg=((218-t,leadpos[1]+9), col,'min','rtl')) # type: ignore
                    render('text', text=format(int(a['score']),',')+' - '+str(int(a["points"]))+'pp ('+str(int(a['combo']))+'x) '+timeform(int(time.time()-a['time'])), arg=((17-t,leadpos[1]+30), col,'min')) # type: ignore
    #                   render('text', text=, arg=((17,leadpos[1]+28), col,'min'))
                     #(((hits[0]*perfbom)+(hits[1]*(perfbom/2))+(hits[2]*(perfbom/3)))*scoremult)-(hits[3]*(perfbom*2))
                    c+=1
        sysbuttonpos=(0,h-60,100,60),(100,h-60+crok,100,60),(200,h-60+crok+crub,100,60), # type: ignore
        if modsani[1]: # Animation for Mod Select :3
            pop=modsani[0].value
        else:
            pop=1-modsani[0].value
        if not modsani[1]:
            mod=0
        get_mods((100,h-(110*(1-pop)))) # type: ignore
        render('rect', arg=((0,h-(180*pop),w,120), (hcol[1]), False),borderradius=10) # type: ignore
        render('rect', arg=((0,h-(170*pop),w,120), (hcol[0]), False),borderradius=10) # type: ignore
        #(340,h-160,90,40) ~ Placeholder
        # This will be here for now, it WILL get better and more optimized over time
        t=(20,20,120,120,220,320,420,480)
        tm=[]
        for b in range(1,len(t)+1): # Ewwwwwww
            if (b == 2 and modsen[2]) or (b == 3 and modsen[1]):#modsen[3]
                tm.append(-999)
            else:
                tm.append(t[b-1])
        mod=menu_draw(((tm[0],h-(160*pop),90,40) # type: ignore
                           ,(tm[1],h-(110*pop),90,40) # type: ignore
                           ,(tm[2],h-(160*pop),90,40) # type: ignore
                           ,(tm[3],h-(110*pop),90,40) # type: ignore
                           ,(tm[4],h-(160*pop),90,40) # type: ignore
#                           ,(tm[5],h-160,90,40)
#                           ,(tm[6],h-160,90,40)
#                           ,(tm[7],h-160,90,40)
                       )
                       ,(modsalias),enabled_button=modsen,styleid=3)
        if mod==1:
            msg='View a perfect play (0)'
        elif mod==2:
            msg="Beat to the rhythm (+1.5)"
        elif mod==3:
            msg='Half blind (+0.5)'
        elif mod==4:
            msg="makes everything easy (/0.5)"
        elif mod==5:
            msg='Adds new fun! (0)'
        elif mod==6:
            msg='Double the fun (+0.5)'
        elif mod==7:
            msg='We be easy on you (/0.5)'
        render('rect',arg=((0,h-65,w,5),hcol[1],False)) # type: ignore
        render('rect', arg=((0,h-60,w,60), hcol[0], False)) # type: ignore
#        for systrocity in sysbuttonpos:
#            render('rect', arg=((systrocity), (100,100,150), True),bordercolor=(80,80,100),borderradius=10)
        if beatmaps: # type: ignore
            gobutton=menu_draw(((w-120,h-60,120,60),),(gotext,),bigmode=True,styleid=3,bradius=0) # type: ignore
        else:
            gobutton=0
        if scoremult==1:
            m='Mods'
        else:
            m=str(scoremult)+'x'
        sysbutton=menu_draw(sysbuttonpos,('Back',m,'Quest'),styleid=3,bradius=0) # type: ignore
        render('rect',arg=((0,h-5,w,5),hcol[1],False)) # type: ignore
        if not qlutaerror: # type: ignore
            coff=80
            render('rect',arg=((w//2-coff-5,(h-90),310,100),hcol[1],False),borderradius=10) # type: ignore
            render('rect',arg=((w//2-coff,(h-75),300,75),hcol[1],False)) # type: ignore
            print_card(totperf,totacc,settingskeystore['username'],(w//2-coff,(h-85)),totrank,isgrayed=restricted) # type: ignore
#        if ranktype and not ranktype==3:
#            if not modshow:
#                of=110
#            else:
#                of=0
#            render('rect', arg=((40,h-200+of,250,25), blend(opacity//2,0), False),borderradius=5)
#            render('text', text='You will not earn Points', arg=((0,0), forepallete,"center"),relative=(40,h-200+of,250,25))
        if not beatani[1] or not diffani[1]: # type: ignore
            cross[0]=beatani[0].value # type: ignore
            cross[1]=diffani[0].value # type: ignore
        if sysbutton==1:
            if not menuback>=30:
                menuback+=backspeed # type: ignore
        else:
            if not menuback<=0:
                menuback-=backspeed # type: ignore
        freeze=0
        tmp=0
        render('header') # type: ignore
        hax=300//2
        if w <= 820 and h<=620: # type: ignore
            popupw=w//2-hax # type: ignore
        else:
            popupw=50
        if beatmaps==0: # type: ignore
            render('text', text='No Beatmap added :sad:', arg=(offset, forepallete)) # type: ignore
        else:
            diffpos=(popupw+20+hax,150)
            #pass#int(len(objects)*perfbom*scoremult)
            render('text', text=songtitle, arg=((20,15), forepallete)) # type: ignore
            render('rect',arg=((popupw-4,76,hax*2,110),blend(opacity,20),False),borderradius=20) # type: ignore
            render('rect',arg=((popupw,80,hax*2,110),blend(opacity,0),False),borderradius=20) # type: ignore
            render('text', text=rankmodes[ranktype][0], arg=((popupw+20+hax,90), rankmodes[ranktype][1])) # type: ignore # Rank Type
            if pp[0]!=pp[1]:
                render('text', text=str(pp[0])+'-'+str(pp[1])+'pp', arg=((popupw+20+hax,120), forepallete)) # type: ignore
            render('text', text='BPM: '+str(int(60000/bpm)+1), arg=((popupw+20,90), forepallete)) # type: ignore # type: ignore
            render('text', text=clockify(int(lastms//1000)/speed), arg=((popupw+20,155), forepallete)) # type: ignore
            render('text', text='+'+format(maxperf,',')+'pp', arg=((popupw+20,120), forepallete)) # type: ignore
            render('rect', arg=((diffpos[0]-(bgcolour//2),diffpos[1],100+bgcolour,30), (levelcol[0]-20,levelcol[1]-20,levelcol[2]-20), False),borderradius=10) # type: ignore
            render('rect', arg=((diffpos[0],diffpos[1],100,30), levelcol, False),borderradius=10) # type: ignore
            render('text', text='Lv. '+str(round(lvrating,2)), arg=((0,0), forepallete,"center"),relative=(diffpos[0],diffpos[1],100,30)) # type: ignore
            textbox((20,44,300),20,text=search[1],center=True,min=True,bg_colour=hcol[0])
def timeform(t):
    if t==None:
        return 'Never Played'
    if t>=31536000:
        x=int(t//31536000)
        fix='yr'
    elif t>=2630000:
        fix='m'
        x=int(t//2630000)
    elif t>=86400:
        x=int(t//86400)
        fix='d'
    elif t>=3600:
        x=int(t//3600)
        fix='h'
    elif t>=60:
        x=int(t//60)
        fix='m'
    elif t<60:
        x=int(t)
        fix='s'
    return str(x)+fix
def preparemap():
    global beatnowmusic,preparedmap
    preparedmap=1
    transitionprep(4) # type: ignore
    resetscore() # type: ignore
