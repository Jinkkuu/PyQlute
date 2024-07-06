import pygame
from data.modules.bootstrap import getactivity,transitionprep
from data.modules.renderapi import draw_button,center_text,getfonts
from data.modules.songselect import getmaxpoints,getmult
from data.modules.colours import maincolour
from data.modules.settings import getsetting

gradecolour=(114, 180, 181),(114, 142, 179),(105, 173, 99),(113, 85, 173),(173, 136, 61),(168, 70, 50),(20,20,20)
testing=0
replaymen=0
def beatres(screen,w,h):
    if getactivity()==9:
        from data.modules.gameplay import points,accuracy,hits
        from data.modules.onlineapi import oldstats,issubmiting,level,totacc,totrank,totperf,totscore,prevrank
        screen.fill(maincolour[0])
        if replaymen:
            title='Replay Screen'
        else:
            title='Results Screen'
        if accuracy>=100:
            gradet='X'
            gc=gradecolour[0]
        elif accuracy>95 and not hits[3]:
            gradet='S'
            gc=gradecolour[1]
        elif accuracy>90:
            gradet='A'
            gc=gradecolour[2]
        elif accuracy>85:
            gradet='B'
            gc=gradecolour[3]
        elif accuracy>69:
            gradet='C'
            gc=gradecolour[4]
        elif accuracy<1:
            gradet='?'
            gc=gradecolour[-1]
        else:
            gradet='D'
            gc=gradecolour[5]
        scale=(w//800,h//600)
        scrop=(w//2-((100//2)*scale[0]),(h//2+50-((460//2)*scale[1])),100*scale[0],50*scale[1])
        pup=[hits[0],hits[1],hits[2],hits[3]]
        pygame.draw.rect(screen,gc,pygame.Rect(scrop),border_radius=20)
        center_text(screen,gradet,(scrop[0],scrop[1]+5,scrop[2],scrop[3]),colour=(255,255,255),type='grade')
        center_text(screen,str(format(int(points/getmaxpoints()*(1000000*getmult())),',')),(scrop[0],scrop[1]+80,scrop[2],scrop[3]),colour=(255,255,255),type='grade')
        center_text(screen,'pp - '+str(str(format(int(points),',')))+'/'+str(str(str(format(getmaxpoints(),',')))),(w//2-150,h//2-30,0,0),colour=(255,255,255))
        center_text(screen,str(accuracy)+'%',(w//2+160,h//2-30,0,0),colour=(255,255,255))
        center_text(screen,'MAX - '+str(pup[0]),(w//2-150,h//2,0,0),colour=(255,255,255))
        center_text(screen,'GREAT - '+str(pup[1]),(w//2+160,h//2,0,0),colour=(255,255,255))
        center_text(screen,'MEH - '+str(pup[2]),(w//2-150,h//2+30,0,0),colour=(255,255,255))
        center_text(screen,'BAD - '+str(pup[3]),(w//2+160,h//2+30,0,0),colour=(255,255,255))
        if issubmiting and getsetting('username'):
            center_text(screen,'Submitting Score...',(scrop[0],scrop[1]+270,scrop[2],scrop[3]),colour=(255,255,255))
        elif getsetting('username'):
            pygame.draw.rect(screen,maincolour[1],pygame.Rect(w//2-110,h//2+43,220,35),border_radius=10)
            center_text(screen,'You are Level '+str(format(level,','))+'!',(w//2,h//2+60,0,0),colour=(255,255,255))
            center_text(screen,'Overall Rank - #'+str(format(totrank,',')),(w//2+160,h//2+95,0,0),colour=(255,255,255))
            center_text(screen,'Overall Points - '+str(format(totperf,',')),(w//2-150,h//2+95,0,0),colour=(255,255,255))
            center_text(screen,'Overall Accuracy - '+str(round(totacc,2))+'%',(w//2-150,h//2+135,0,0),colour=(255,255,255))
            center_text(screen,'Ranked Score - '+str(format(totscore,',')),(w//2+160,h//2+135,0,0),colour=(255,255,255))
            changed=[totrank-prevrank,totperf-oldstats[0],round(totacc-oldstats[2],2),totscore-oldstats[1],level-oldstats[3]]
            final=[totrank,totperf,totacc,totscore,level]
            klap=(w//2+200,h//2+105),(w//2-121,h//2+105),(w//2-109,h//2+145),(w//2+160,h//2+145),(w//2+45,h//2+68,0,0)
            for a in range(1,len(changed)+1):
                cha=(255, 155, 128),(186, 255, 171)
                if changed[a-1]<0:
                    chap=''
                    if a in (1,5):
                        chac=cha[1]
                    else:
                        chac=cha[0]
                elif changed[a-1]>0:
                    if a ==1:
                        chac=cha[0]
                        chap='-'
                    else:
                        chap='+'
                        chac=cha[1]
                if changed[a-1]!=final[a-1] and changed[a-1]!=0:
                    if a==3:
                        suf='%'
                    else:
                        suf=''
                    fip=format(changed[a-1],',')
                    if a == 1:
                        if chac==cha[1]:
                            fip=fip.replace('-','+')
                    screen.blit(getfonts(0).render(chap+str(fip)+suf,True,chac),klap[a-1])
        else:
            center_text(screen,'Hey, Your not Logged in yet!',(scrop[0],scrop[1]+270,scrop[2],scrop[3]))
            center_text(screen,'You can compete if you Log in~',(scrop[0],scrop[1]+290,scrop[2],scrop[3]))

        screen.blit(getfonts(0).render(title,True,(255,255,255)),(20,20))
        butt=draw_button(screen,((scrop[0]-90,scrop[1]+360,scrop[2]*3-20,scrop[3]),),('Continue',))
        if butt:
            transitionprep(2)