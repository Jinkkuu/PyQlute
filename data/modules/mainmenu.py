mtext='Play','Edit','Browse','Leave'#,'TB'
toptext='Settings','Account','Downloads'
menupos=[]
opacity=10
bgdefaultcolour=(45,47,100)
mainmenucolor=(67, 124, 191),(92, 90, 145),(179, 72, 62)
dcolour=(40,40,40) # default colour for top bar and blades~
accounts=0
osam=0
for a in range(1,len(mtext)+1):
    menupos.extend([0])
def mainmenu():
    global debugmode, activity,beatnowmusic, totperf,totscore,msg,menubutton,topbutton,accounts,bladeani,background
    if not bladeani[1] and activity==1:
        bladeani[1]=1
        bladeani[0].start()
    elif activity!=1:
        bladeani[1]=0
    if activity==1:
        bladeani[0].update()
        try:
            if background and settingskeystore['bgmm']:
                screen.blit(background, (0,0))
        except Exception as err:
            print(err)
            background=0
        mmenu=[]
        tmenu=[]
        #wid=90*(w//640)
        wid=90*2
        hei=150
        scale=0.9
        wod=45
        if wid>90*2:
            wid=90*2
        ani=((100-bladeani[0].value)/100)
        bla=(ani*w)
        anib=bladeani[0].value/100
        for a in range(1,len(mtext)+1):
            mmenu.append((bla+(w//2-((wid*scale)*(len(mtext)/2))+((wid*scale)*(a-1))),h//2-(75*scale),wid*scale,hei*scale))
        for a in range(1,len(toptext)+1):
            tmenu.append((w-((20*7)*(a))+24,0,20*7,wod))
        drawRhomboid(screen,dcolour,bla-25,h//2-(76*scale),w+80,hei*scale,26)
        menubutton=menu_draw(mmenu, text=mtext,isblade=True,ishomemenu=True)
#        for a in range(1,len(rankdiffc)+1):
#            render('rect',arg=((0+(60*(a-1)),h-150,50,20),rankdiffc[a-1],False),borderradius=20)
#        render('text', text=gametime/lastms, arg=((20,h-80), forepallete))
        #print(1-((gametime/(lastms+1000))))
        if gametime>=lastms+1000 or gametime<=-1:
            song_change(1)
        if beatmaps!=0:
            render('text', text=songtitle, arg=((20,anib*55), forepallete))
        else:
            render('text', text='nothing...', arg=((20,anib*55), (255,255,255)))
        render('rect',arg=((0,0,w,45),dcolour,False))#,surf=surface[0])
        topbutton=menu_draw(tmenu, text=toptext,isblade=True,ignoremove=True,ishomemenu=True)
        if not qlutaerror:
            print_card(totperf,totacc,settingskeystore['username'],(w//2-150,h//2+120),totrank,home=True,isgrayed=restricted)
        if menunotice!='':
            tmp = fonts[0].render(str(menunotice),  True,  (0,0,0))
            txtrect=tmp.get_rect()
            render('rect',arg=((w//2-(txtrect[2]//2)-10,h//2-170,txtrect[2]+20,50),(bgdefaultcolour[0]+25,bgdefaultcolour[1]+25,bgdefaultcolour[2]+25),False),borderradius=10)
            render('text',text=menunotice,arg=((20, 20),(255,255,255),'center'),relative=(w//2-(txtrect[2]//2)-10,h//2-170,txtrect[2]+20,50))
        if totrank==1:
            t=2
        else:
            t=1
        #print_card(oneperf,oneperf*10*10*300,'Monstras',(340,60),t)
        rank=2
        b=1
        #print_card(totperf//2,totscore//2,'MiXer',(340,60),2,isgrayed=1)
        if gamever!='0.0.0':
            render('text', text=gamename+'/'+gameedition+' ('+str(gamever)+')', arg=((0,0), forepallete,'center'),relative=(w//2,h-35,0,0))
        else:
            render('text', text='Local release', arg=((0,0), (255,255,0),'center'),relative=(w//2,h-35,0,0))
        if menubutton == 1:
            msg=' You have '+str(format(beatmaps,','))+' Songs '
        elif menubutton == 2:
            msg='Time to make beatmaps!'
        elif menubutton == 3:
            msg='Browse our catalog'
        elif menubutton == 4:
            msg='See ya next time~'

#        render('rect', arg=((-10,150,350,60), (maxt(40,bgcolour),maxt(40,bgcolour),maxt(100,bgcolour)), False),borderradius=10)
#        render('text', text='WILL CHANGE', arg=((25,155), (255,255,maxt(0,bgcolour)),'grade'))
        song_progress()
