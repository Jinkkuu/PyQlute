import pygame
notewidth=100
noteheight=30
osam=0
def render(type, arg=(0, 0) ,  text='N/A', bordercolor=forepallete, borderradius=0,relative=(0,0,0,0),surf=''):
    off=0
    grad2=False
    if surf=='':
      surf=screen
    try:
        bordercolor=mint(bordercolor[0],darkness),mint(bordercolor[1],darkness),mint(bordercolor[2],darkness)
        try:
            colour=mint(arg[1][0],darkness),mint(arg[1][1],darkness),mint(arg[1][2],darkness)
        except Exception:
            colour=mint(arg[1],darkness)
        if type == 'text':
            if "bold" in arg:
                ftype=3
            elif "min" in arg:
                ftype=1
            elif "grade" in arg:
                ftype=2
            else:
                ftype=0
            tmp = fonts[ftype].render(str(text),  True,  colour)
            txtrect=tmp.get_rect()
            if "center" in arg:
                relative=pygame.Rect(relative)
                out = tmp.get_rect(center=relative.center)
            else:
                out=arg[0]
                if "rtl" in arg:
                    out=out[0]-txtrect[2],out[1]
            if "tooltip" in arg:
                render('rect', arg=((out[0]-2,out[1]-2,txtrect[2]+4,txtrect[3]+4), (50,50,50), False),borderradius=5)
            surf.blit(tmp,  out)
            return tmp.get_rect()
        elif type == 'clear':
            screen.fill(arg)
        elif type == 'line':
            pygame.draw.line(surf,colour,arg[0],arg[2])
        elif type == 'rect':
            pygame.draw.rect(surf, colour, (arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), border_radius=borderradius)
            if arg[2]:
                pygame.draw.rect(surf, bordercolor, (arg[0][0], arg[0][1], arg[0][2]-off, arg[0][3]-off), 1, border_radius=borderradius)
            ## This was for a "Wireframe" Like Square
#            pygame.draw.rect(screen, (0, 255, 0), (arg[0][0], arg[0][1], arg[0][2], arg[0][3]), 1)
        else:
            crash('Render unsupported Type')
    except Exception as error:
        print(error)
        exit()
        crash(str(error)+' (renderer)')
def menu_draw(instruction, text=None,forcetext=False,usecolour=False,align=1,iconoffset=(0,0),textoffset=(0,0),showicon=False,newline=' - ',crossid=0,bradius=10,settings=False,beatmenu=0,ishomemenu=False,ignoremove=False, istextbox=False, selected_button=0,enabled_button=[],enable_border=False, hidebutton=False,bigmode=False,startlimit=1,endlimit=None,styleid=1,isblade=False,icon=0):
    global osam
    fmove=0
    pmove=0
    moveid=0
    if endlimit==None:
        endlimit=len(instruction)
    elif endlimit>=len(instruction):
        endlimit=len(instruction)
    if startlimit<1:
        startlimit=1
    button=0
    if istextbox:
        button=0, 0, 0
    else:
        if settings or styleid==3:
            buttonc=82,80,135
            tcol=forepallete
        elif styleid==0:
            buttonc=30, 100, 120
            tcol=255,255,255
        elif styleid==1:
            buttonc=bgdefaultcolour[0]+15,bgdefaultcolour[1]+15,bgdefaultcolour[2]+15
            tcol=255,255,255
        elif styleid==2:
            buttonc=219, 219, 219
            tcol=0,0,0
    select=False
    for a in range(startlimit,  endlimit+1):
        tmp=instruction[a-1]
        if not beatmenu:
            tmp=pygame.Rect(tmp[0],tmp[1],tmp[2],tmp[3])
        else:
            size=65
            tmp=pygame.Rect(w-tmp[2]+80,(h//2)-tmp[1]-((size+5)*cross[crossid])+((size+5)*(a-1)),tmp[2],tmp[3])
        if tmp.collidepoint(pygame.mouse.get_pos()) and not select:
            select=True
            buttcolour = (buttonc[0]+10,buttonc[1]+10,buttonc[2]+10)
            if pygame.mouse.get_focused():
                button=a
            else:
                osam=0
        else:
            buttcolour = buttonc
        b = (102,100,175)
        #drawRhomboid(screen, (255,255,255), 50, 50, 300, 200, 100, 3)
        if not hidebutton:
            if usecolour:
                if a==1:
                    buttcolour=mainmenucolor[0]
                elif text[a-1] in ('Leave','Back'):
                    buttcolour=mainmenucolor[2]
                else:
                    buttcolour=mainmenucolor[1][0]-(10*(a-2)),mainmenucolor[1][1]-(10*(a-2)),mainmenucolor[1][2]-(10*(a-2))
            if button==a:
                buttcolour=buttcolour[0]+5,buttcolour[1]+5,buttcolour[2]+5

            if not isblade:
                if selected_button==a or (enabled_button!=[] and enabled_button[a-1]):
                    buttcolour=b
                if settings:
                    render('rect', arg=(tmp, buttcolour, False))
                else:
                    render('rect', arg=((tmp), buttcolour, False),borderradius=bradius)
            else:
                if ishomemenu:
                    if not ignoremove:
                        moveid=menupos[a-1][0].value
                        if a!=len(menupos):
                            pmove=menupos[a][0].value//2
                        fmove=menupos[a-2][0].value//2
                        
                        if button==a:
                            if not menupos[a-1][1]:
                                menupos[a-1][0]=Tween(begin=moveid, end=20,duration=mdur,easing=measetype,easing_mode=EasingMode.OUT)
                                menupos[a-1][1]=1
                                menupos[a-1][0].start()
                        elif button!=a:
                            if menupos[a-1][1]:
                                menupos[a-1][0]=Tween(begin=moveid, end=0,duration=mdur,easing=measetype,easing_mode=EasingMode.OUT)
                                menupos[a-1][1]=0
                                menupos[a-1][0].start()
                drawRhomboid(screen, buttcolour, fmove+tmp[0]-(moveid//2)-pmove, tmp[1], tmp[2]+moveid, tmp[3],25, 0)
            if not text == None:
                if icon and icon[a-1]!=None:
                    showicon=1
                    end=icon[a-1].get_rect(center=pygame.Rect((fmove+tmp[0]-pmove+iconoffset[0],tmp[1]+iconoffset[1],tmp[2],tmp[3])).center)
                    screen.blit(icon[a-1], (end[0],end[1]))
                else:
                    showicon=0
                if bigmode:
                    if not showicon:
                        render('text', text=text[a-1], arg=((0,0), forepallete,'center','grade'),relative=tmp)
                else:
                    if ishomemenu:
                        home=moveid
                    else:
                        home=0
                    if not showicon or forcetext:
                        if not settings:
                            s=text[a-1].split(newline)
                            d=instruction[a-1][3]//len(s)
                            f=0
                            for e in s[::-1]:
                                if ishomemenu:
                                    sd=0
                                else:
                                    sd=(d*f)
                                if align:
                                    ali='center'
                                else:
                                    ali='nada'
                                render('text', text=e.replace('[no video]','').rstrip(' '), arg=((fmove+tmp[0]-pmove+textoffset[0],tmp[1]+textoffset[1]+sd), tcol,ali),relative=(fmove+tmp[0]-pmove+textoffset[0],tmp[1]+textoffset[1]+sd,tmp[2],d))
                                f+=1
                        else:
                            render('text', text=text[a-1], arg=((0,0), forepallete,'center','min'),relative=tmp)
    return button
def clear(color):screen.fill(color)
def blend(opacity,bgcolour):
    return maxt(bgdefaultcolour[0]-opacity,bgcolour),maxt(bgdefaultcolour[1]-opacity,bgcolour),maxt(bgdefaultcolour[2]-opacity,bgcolour)

def drawRhomboid(surf, color, x, y, width, height, offset, thickness=0):
    points = [
        (x + offset, y), 
        (x + width + offset, y), 
        (x + width-offset, y + height), 
        (x-offset, y + height)]
    pygame.draw.polygon(surf, color, points, thickness)
def fullscreenchk():
    global w, h, w, h,background,fieldpos,modsv,loading, bani,beatani,diffani,screen,reload,transani,modsani, button_size_width, firstcom,tal,keymap,fonts,fontsb,volani,noteheight,logopos,bladeani
    reload=False
    if not settingskeystore['fullscreen']:
        if not firstcom:
            w=800
            h=600
            screenw=w
            screenh=h
    else:
        if not firstcom:
            w=0
            h=0
            screenh=0
            screenw=0

    flags=pygame.RESIZABLE
    bit=24
    if settingskeystore['fullscreen']:
        if not firstcom:
            screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN|flags, bit)
            reload=True
    else:
        if not firstcom:
            screen=pygame.display.set_mode((w, h), flags, bit)
            reload=True
    if screen.get_size()[0]!=w and screen.get_size()[0]>=800:
        reload=True
    elif screen.get_size()[1]!=h and screen.get_size()[1]>=600:
        reload=True
    if not firstcom:
        firstcom=True
        beatani=[Tween(begin=cross[0], end=beatsel,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
        beatani[0].start()
        diffani=[Tween(begin=-1, end=0,duration=1,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
        diffani[0].start()
        bladeani=[Tween(begin=0, end=101,duration=500,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
        bani=Tween(begin=0, end=1,duration=200,easing=Easing.CUBIC,easing_mode=EasingMode.OUT,boomerang=1)
        modsv=0
        modsani=[Tween(begin=0, end=1,duration=350,easing=Easing.CUBIC,easing_mode=EasingMode.OUT),0]
        modsani[0].start()
        transani=[Tween(begin=0, end=1,duration=150*2,easing=Easing.CUBIC,easing_mode=EasingMode.OUT,boomerang=True),0]
        loading=Tween(begin=0, end=1,duration=1000,easing=Easing.BOUNCE,easing_mode=EasingMode.OUT,boomerang=True,loop=True)
        loading.start()
        volani=Tween(begin=volvisual, end=vol,duration=250,easing=Easing.CUBIC,easing_mode=EasingMode.OUT)
        volani.start()
    ins=1
    if reload:
        if screen.get_width()<800:
            w=800
        else: 
            w=screen.get_width()
        if screen.get_height()<600:
            h=600
        else: 
            h=screen.get_height()
        f=24
        fonts = pygame.font.Font(fontname['default'],  int(f//1.2)),pygame.font.Font(fontname['default'],  f//2),pygame.font.Font(fontname['default'],  f*2),pygame.font.Font(fontname['bold'],  int(f)),pygame.font.Font(fontname['default'],  int(f/1.1))
        button_size_width=w//2
        reloadbg()
    tal=25*(w/25)//len(bars)
    scroll=h-30-noteheight
    fieldpos=(w//2,0)
    #scroll=h//2
    #keymap=((w//2-(50*4),scroll,100,noteheight),(w//2-(50*2),scroll,100,noteheight),(w//2-(50*0),scroll,100,noteheight),(w//2-(50*-2),scroll,100,noteheight),)
    keymap=((-(50*4),scroll,100,noteheight),(-(50*2),scroll,100,noteheight),(-(50*0),scroll,100,noteheight),(-(50*-2),scroll,100,noteheight),)