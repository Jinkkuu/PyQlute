from data.modules.onlineapi import restrictedmsg,togsign,rsus,reloadprofile
from data.modules.input import get_input
from data.modules.colours import maincolour
from data.modules.renderapi import getfonts,draw_button,textbox
from data.modules.bootstrap import getactivity,transitionprep,notification
from data.modules.settings import getsetting,setsetting
import pygame,threading,sys,os,hashlib
textboxid=0
logintext=['','']
restricted=0
maxletters=30
profilehealth=0
usrtxt=getfonts(0).render('Username:',True,(255,255,255)) , getfonts(0).render('Password:',True,(255,255,255))
def loginscreen(screen,w,h):
    global sysbutton,l,logbutton,logintext,textboxid
    from data.modules.onlineapi import restricted,issigned
    if getactivity()==7:
        pygame.draw.rect(screen,(20,20,20),(0,0,w,h))
        pygame.draw.rect(screen,maincolour[2],(0,h-60,w,60))
        screen.blit(getfonts(2).render('Login',True,(255,255,255)),(20,20))
        if restricted:
            logbutton=0
            screen.blit(getfonts(0).render('Your client has been locked!',True,(255,255,255)),(20,80))
            screen.blit(getfonts(0).render(restrictedmsg,True,(255,255,255)),(20,110))
        else:
            if issigned:
                screen.blit(getfonts(0).render('You are logged in as '+str(getsetting('username')),True,(255,255,255)),(20,80))
                logbutton=draw_button(screen,((w//2-60,h//2+90,120,40),),('Log out',),border_radius=10) 
                for event in get_input(): 
                    if logbutton==1:
                        if issigned:
                            setsetting('username',None)
                            setsetting('password',None)
                            logintext[1]=''
                            togsign()
                            rsus()
                            notification('QlutaBot',desc='You are offline')
            else:
                if textboxid:
                    l=[(255,255,255),(105,255,105)]
                else:
                    l=[(105,255,105),(255,255,255)]
                id=0
                for a in logintext:
                    if len(a)>=maxletters:
                        logintext[id]=logintext[id][:maxletters]
                    id+=1
                screen.blit(usrtxt[0],(w//2-300,h//2-80))
                screen.blit(usrtxt[1],(w//2-300,h//2))
                textbox(screen,(w//2-300,h//2-50,600),40,text=logintext[0],border_colour=l[0],center=True)
                textbox(screen,(w//2-300,h//2+30,600),40,text='*'*len(logintext[1]),border_colour=l[1],center=True)
                logbutton=draw_button(screen,((w//2-160,h//2+90,120,40),(w//2+20,h//2+90,120,40),),('Log in','Sign Up'),border_radius=10)
                for event in get_input():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            textboxid=not textboxid
                        elif event.key == pygame.K_BACKSPACE: 
                            logintext[textboxid] = logintext[textboxid][:-1]
                        else:
                            logintext[textboxid] += event.unicode
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if logbutton==1:
                            if logintext[0]!='' or logintext[1]!='':
                                setsetting('username',logintext[0])
                                setsetting('password',hashlib.sha256(bytes(logintext[1],'utf-8')).hexdigest())
                                threading.Thread(target=reloadprofile).start()
                            else:
                                notification('Qluta',desc='what u doin >:^')
                        elif logbutton==2:
                            if sys.platform=='win32':
                                os.startfile(getsetting('apiurl')+'signup')
                            elif sys.platform=='darwin':
                                os.system('open '+getsetting('apiurl')+'signup')
                            else:
                                try:
                                    os.system('xdg-open '+getsetting('apiurl')+'signup')
                                except OSError:
                                    pass                            
        sysbutton=draw_button(screen,((0,h-60,100,60),),('Back',),border_radius=0)
        if sysbutton:
            transitionprep(1)



