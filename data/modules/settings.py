import json
fpsmodes=[30,60,120,240,480,1000]
settingstemplate={
        'hitsound' : True,
        'leaderboard' : True,
        'fullscreen' : False,
        'effects' : True,
        'skinning' : True,
        'username' : None,
        'password' : None,
        'apiurl' : 'https://qlute.pxki.us.to/',
        'bgmm' : True,
        'sreplay':True,
        'fps' : 480,
        'Key1' : 'd',
        'Key2' : 'f',
        'Key3' : 'j',
        'Key4' : 'k'
    }
def reloadsettings():
    tmp=open(datapath+'settings', 'w')
    tmp.write(json.dumps(settingskeystore))
    tmp.close()
if os.path.isfile(datapath+'settings'):
    print('Using SettingsV2...')
    settingskeystore=json.load(open(datapath+'settings'))
    for a in settingstemplate:
        if not a in settingskeystore:
            settingskeystore[a]=settingstemplate[a]
            reloadsettings()
    print('Completed')
else:
    settingskeystore=settingstemplate
fpsmode=fpsmodes.index(settingskeystore['fps'])
print(fpsmode,settingskeystore['fps'])
setupid=1
setupcatagory=('General','Skinning','Audio','Graphics','Debug','Account')
setupcatpos=[]
b=0
customid=0
for a in setupcatagory:
    setupcatpos.append((0+(100*b),80,100,20))
    b+=1
#                            render('rect', arg=(pos, (43, 163, 237), False))
successfulsignin=0
if settingskeystore['username'] and settingskeystore['password']:
    issigned=1
else:
    issigned=0
def customization():
    global sysbutton
    if activity==11:
        if customid==1:
            uid='Note Width'
        elif  customid==2:
            uid='Note Height'
        else:
            uid='N/A'
        render('rect', arg=((0,0,w,h), (42,40,95), False))
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        render('rect', arg=((0,0,w,100), (62,60,115), False))
        render('text', text='(Experimental) Customization - '+str(uid), arg=(offset, forepallete,'grade'))
        render('rect', arg=(((w//2)-(notewidth//2),(h//2)-(noteheight//2),notewidth,noteheight), notecolour, False))
        if customid==1:
            render('text', text='WIDTH ('+str(notewidth)+')', arg=((0,0), forepallete,'center'),relative=((w//2)-(notewidth//2),(h//2)-(noteheight//2)-20,notewidth,0))
            render('text', text='Adjust by using arrow keys LEFT / RIGHT', arg=((0,0), forepallete,'center'),relative=((w//2)-(notewidth//2),(h//2)-(noteheight//2)+noteheight+20,notewidth,0))
        elif customid==2:
            render('text', text='HEIGHT ('+str(noteheight)+')', arg=((0,0), forepallete,'center'),relative=((w//2)-(notewidth//2),(h//2)-(noteheight//2)-20,notewidth,0))
            render('text', text='Adjust by using arrow keys UP / DOWN', arg=((0,0), forepallete,'center'),relative=((w//2)-(notewidth//2),(h//2)-(noteheight//2)+noteheight+20,notewidth,0))

        sysbutton=menu_draw(((-10,h-60,100,60),),('Back',),bradius=0,styleid=3)
cset=0
def controlsetup():
    global sysbutton,cset
    if activity==13:
        render('rect', arg=((0,0,w,h), (42,40,95), False))
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        render('text', text='Controls', arg=((20,20), forepallete,'grade'))
        render('text', text='Click the one you want to change', arg=((20,80), forepallete))
        sysbutton=menu_draw(((-10,h-60,100,60),(w//2-160,h//2-80,80,80),(w//2-80,h//2-80,80,80),(w//2,h//2-80,80,80),(w//2+80,h//2-80,80,80),),('Back',settingskeystore['Key1'].upper(),settingskeystore['Key2'].upper(),settingskeystore['Key3'].upper(),settingskeystore['Key4'].upper()),bradius=0,styleid=3,selected_button=cset+1)
def settingspage():
    global settingskeystore, activity,catbutton, screen, firstcom, change, fpsmode,totperf,totscore,msg,logotime,setbutton,sysbutton
    if activity==2:
        #settingskeystore[2], settingskeystore[1], fullscreen
        if str(fpsmodes[fpsmode])!='1000':
            tmp=str(fpsmodes[fpsmode])
        else:
            tmp='Unlimited'
        if not settingskeystore['username']:
            user='Guest'
        else:
            user=settingskeystore['username']
        setuplist={'general': {'Leaderboards':settingskeystore['leaderboard'],'Effects':settingskeystore['effects'],'Save Replays':settingskeystore['sreplay'],'Enable BG':settingskeystore['bgmm'],'Controls':'->'},'skinning':{'Change Skins':'->','Note Width':'->','Note Height':'->','Note Colour':'->','Background Colour':'->','HealthBar Colour':'->','Insanity Level':'->',},'audio':{'Hitsounds':settingskeystore['hitsound']},'graphics':{'FPS':tmp,'Fullscreen':settingskeystore['fullscreen']},'debug':{},'account':{'Username':user}}
        #setuplist=['FPS: '+tmp,'Fullscreen: '+str(settingskeystore['fullscreen']),'Effects: '+str(settingskeystore['effects']),'Allow Skins: '+str(settingskeystore['skinning']),'Hitsounds: '+str(settingskeystore['hitsound']),'Leaderboards: '+str(settingskeystore['leaderboard']),'Debug Info','Crash Test']
        setuplistpos=[]
#        for a in range(1,6):
#            setuplist.append('Unknown')
        b=0
        render('rect', arg=((0,0,w,h), (42,40,95), False))
        if setupid==2:
            render('rect', arg=((w-400,100,400,h-100), (20,20,20), False))
            showplayfield((w-200,-30))
            render('rect', arg=((w-380,110,200,10), (0,180,0), False),borderradius=10)
            render('rect', arg=((w-400,320,100,30), (notecolour), False),borderradius=0)
            render('rect', arg=((w-400+200,250,100,30), (notecolour), False),borderradius=0)
        if setupid==5:
            render('text',text='Game Name - '+str(gamename),arg=((20,120+(23*0)),forepallete))
            render('text',text='Game Version - '+str(gamever),arg=((20,120+(23*1)),forepallete))
            render('text',text='Slyph Engine Version - '+str(sylphenginever),arg=((20,120+(23*2)),forepallete))
            render('text',text='Module Initial Time - '+str(moduletime),arg=((20,120+(23*3)),forepallete))
            render('text',text='Ping Speed - '+str(pingspeed)+'ms',arg=((20,120+(23*4)),forepallete))
            render('text',text='OS - '+str(ostype),arg=((20,120+(23*5)),forepallete))
        else:
            setuptxt=[]
            for a in setuplist[setupcatagory[setupid-1].lower()]:
                b+=1
                poof=offset[1]+40
                if setupid==2:
                    posw=20
                else:
                    posw=w//2-110
                text=str(setuplist[setupcatagory[setupid-1].lower()][a])
                if '->' in text:
                    sp=' '
                else:
                    sp=' : ' 
                setuplistpos.append((posw,  poof+(50*b),  220,  button_size_height))
                setuptxt.append(a+sp+text)
            if len(setuptxt)<1:
                setbutton=0
            else:
                setbutton=menu_draw((setuplistpos), (setuptxt),styleid=3)
            if setbutton == 1 and setupid==4:
                msg='Changes how fast this game goes'
            elif setbutton == 2 and setupid==4:
                msg='Makes the Screen Fullscreen, what do you expect'
            elif setbutton == 2 and setupid==1:
                msg='Changes the Flashing Effect'
            elif setbutton == 1 and setupid==3:
                msg='Enable Hitsounds'
            elif setbutton == 1 and setupid==1:
                msg='Enable Leaderboards'
            elif setbutton == 3 and setupid==1:
                msg='Auto Save Replays'
            elif setbutton == 4 and setupid==1:
                msg="Show song's Background at the main menu"
            elif setbutton == 5 and setupid==1:
                msg='Change your controls for your gameplay'
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        render('rect', arg=((0,0,w,100), (62,60,115), False))
#        b=0
        catbutton=menu_draw((setupcatpos), (setupcatagory),settings=True,selected_button=setupid)
#        for a in setupcatagory:
#            pos=(0+(100*b),80,100,20)
#            render('rect', arg=(pos, (43, 163, 237), False))
#            render('text', text=a, arg=((0,0), forepallete,'center','min'),relative=pos)
#            b+=1
        render('text', text='Settings', arg=(offset, forepallete,'grade'))
        sysbutton=menu_draw(((-10,h-60,100,60),),('Back',),bradius=0,styleid=3)
