mtext=('Play','Edit','Browse','Leave'),('Solo','Multi','Back')
meid=0
meidt=meid
toptext='Settings','Account','Downloads'
opacity=10
bgdefaultcolour=(45,47,100)
mainmenucolor=(67, 124, 191),(92, 90, 145),(179, 72, 62)
dcolour=(40,40,40) # default colour for top bar and blades~
accounts=0
wod=45
def mainmenu():
    global debugmode, meid,osam,activity,beatnowmusic, totperf,totscore,msg,menubutton,topbutton,accounts,bladeani,background
    if not bladeani[1] and activity==1:
        bladeani[1]=1
        bladeani[0].start()
    elif activity!=1:
        bladeani[1]=0
    if activity==1:
        bladeani[0].update()
        if bani.value==1:
            meid=meidt
        bani.update()
        ba=bani.value*w
        if meid:
            ba=-ba
        try:
            if background and settingskeystore['bgmm']:
                screen.blit(background, (0,0))
        except Exception as err:
            print(err)
            background=0
        mmenu=[]
        #wid=90*(w//640)
        wid=90*2
        hei=149
        scale=0.9
        if wid>90*2:
            wid=90*2
        ani=((100-bladeani[0].value)/100)
        bla=(ani*w)
        anib=bladeani[0].value/100
        tmenu=[]
        for a in range(1,len(toptext)+1):
            tmenu.append((w-(45*a),0,45,wod))
        for a in range(1,len(mtext[meid])+1):
            mmenu.append((ba+bla+(w//2-((wid*scale)*(len(mtext[meid])/2))+((wid*scale)*(a-1))),h//2-(75*scale),wid*scale,hei*scale))
        drawRhomboid(screen,dcolour,bla-25,h//2-(76*scale)+1,w+80,hei*scale,26)
        menubutton=menu_draw(mmenu, text=mtext[meid],isblade=True,textoffset=(-10,25),iconoffset=(-7,-5),icon=micon[meid],ishomemenu=True,forcetext=True,usecolour=True)
        if gametime>=lastms+1000 or gametime<=-1:
            song_change(1)
        render('rect',arg=((0,0,w,45),dcolour,False))#,surf=surface[0])
        if beatmaps!=0:
            render('text', text=songtitle, arg=((20,(trans*41)-30), forepallete))
        else:
            render('text', text='nothing...', arg=((20,(trans*41)-30), (255,255,255)))
        render('text',text=gameauthor+' ('+str(copyrightdate[0])+'-'+str(copyrightdate[1])+')',arg=((20, 60),(255,255,255),'min'))
        topbutton=menu_draw(tmenu, text=toptext,ignoremove=True,ishomemenu=True,bradius=0,usecolour=True,icon=(icons['settings.png'],icons['user.png'],icons['download.png']))
        if not qlutaerror:
            print_card(totperf,totscore,settingskeystore['username'],(w//2-150,h//2+120),totrank,home=True,isgrayed=restricted)
        if menunotice!='':
            tmp = fonts[0].render(str(menunotice),  True,  (0,0,0))
            txtrect=tmp.get_rect()
            render('rect',arg=((w//2-(txtrect[2]//2)-10,h//2-170,txtrect[2]+20,50),(bgdefaultcolour[0]+25,bgdefaultcolour[1]+25,bgdefaultcolour[2]+25),False),borderradius=10)
            render('text',text=menunotice,arg=((20, 20),(255,255,255),'center'),relative=(w//2-(txtrect[2]//2)-10,h//2-170,txtrect[2]+20,50))
        if totrank==1:
            t=2
        else:
            t=1
        b=1
        if gamever!='0.0.0':
            render('text', text=gamename+'/'+gameedition+' ('+str(gamever)+')', arg=((0,0), forepallete,'center'),relative=(w//2,h-35,0,0))
        else:
            render('text', text='Local release', arg=((0,0), (255,255,0),'center'),relative=(w//2,h-35,0,0))
        if menubutton == 1:
            msg=' You have '+str(format(beatmaps,','))+' Songs '
        elif menubutton == 2 and meid:
            msg='Play with the world!'
        elif menubutton == 2 and not meid:
            msg='Time to make beatmaps!'
        elif menubutton == 3 and not meid:
            msg='Browse our catalog'
        elif menubutton == 4 and not meid:
            msg='See ya next time~'
        if osam!=menubutton:
            osam=menubutton
            pygame.mixer.Sound(samplepath+'hover.wav').play()
        song_progress()


