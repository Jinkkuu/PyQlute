import pygame, pygame.gfxdraw
from data.modules.bootstrap import getimg
from data.modules.colours import maincolour
from tweener import *
mainmenucolor=(67, 124, 191),(92, 90, 145),(179, 72, 62)
def initscreen(): # Initialize the screen
    from data.modules.bootstrap import resource_path,getsysdata,getname,version
    t=pygame.display.set_mode((800,600),pygame.RESIZABLE)
    name=getname()
    pygame.display.set_caption(f'{name[0]}/{name[1]} {version()[0]}')
    pygame.display.set_icon(pygame.image.load(getsysdata()+'icon.png'))
    return t
def initfont():
    from data.modules.bootstrap import getsysdata,fontpath
    pygame.font.init()
    fontname={'default':fontpath+'default.otf','bold':getsysdata()+'fonts/defaultbold.ttf','score':getsysdata()+'fonts/score.ttf'}
    return pygame.font.Font(fontname['default'],  int(20)),pygame.font.Font(fontname['default'],  12),pygame.font.Font(fontname['default'],  48),pygame.font.Font(fontname['bold'],  int(24)),pygame.font.Font(fontname['score'],  int(48))

fonts=initfont() # Loads up the fonts
def getfonts(value):
    try:
        return fonts[value]
    except KeyError:
        return 0
def textbox(screen,pos,size,text='',center=False,min=False,border_colour=(255,255,255),bg_colour=(40,40,40)):
    hw=(pos[0],pos[1],pos[2],size)
    if center:
        c='center'
    else:
        c=''
    if min:
        b='min'
    else:
        b=''
    pygame.draw.rect(screen,bg_colour,hw)
    pygame.draw.rect(screen,border_colour,hw,2)
    center_text(screen,text,hw,type=(c,b))
    
def draw_button(surface,buttonpos,buttontext,theme=None,enabled_button=[],fonttype=0,selected_button=None,textoffset=(0,0),iconoffset=(0,0),icon=None, isblade=0,border_radius=10,hidetext=0,return_hover=0): # Draws the buttons on the screen and returns a value if it gotten clicked
    from data.modules.input import get_input
    id=1
    clicked=0
    hoverid=-1
    for button in buttonpos:
        buttonrect=pygame.Rect(button)
        mouse=pygame.mouse.get_pos()
        if (len(enabled_button)>=id and enabled_button[id-1]) or selected_button == id:
            sid=7
        else:
            sid=6
        if pygame.Rect.collidepoint(buttonrect,mouse[0],mouse[1]):
            hover=20
            hoverid=id-1
        else:
            hover=0
#        if theme in img and not hover:
#            surface.blit(img[theme],(buttonrect[:2]))
#        elif theme.split('.')[0]+'-hovered.png' in img and hover:
#            surface.blit(img[theme.split('.')[0]+'-hovered.png'],(buttonrect[:2]))
#        else:
        if isblade:
            if id==1:
                buttcolour=mainmenucolor[0]
            elif buttontext[id-1] in ('Leave','Back'):
                buttcolour=mainmenucolor[2]
            else:
                buttcolour=mainmenucolor[1][0]-(10*(id-2)),mainmenucolor[1][1]-(10*(id-2)),mainmenucolor[1][2]-(10*(id-2))
            drawRhomboid(surface, (buttcolour[0]+hover,buttcolour[1]+hover,buttcolour[2]+hover), buttonrect[0],buttonrect[1],buttonrect[2],buttonrect[3],25, 0)
        else:
            pygame.draw.rect(surface,(maincolour[sid][0]+hover, maincolour[sid][1]+hover, maincolour[sid][2]+hover),buttonrect,border_radius=border_radius)
        if icon and icon[id-1]:
            ic=getimg(icon[id-1])
            cen=ic.get_rect(center=buttonrect.center)
            surface.blit(ic,(cen[0]+iconoffset[0],cen[1]+iconoffset[1])) #
        if not hidetext:
            text=getfonts(fonttype).render(buttontext[id-1],True,(255,255,255))
            textpos=text.get_rect(center=buttonrect.center)
            surface.blit(text,(textpos[0]+textoffset[0],textpos[1]+textoffset[1]))
        for event in get_input():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.Rect.collidepoint(buttonrect,mouse[0],mouse[1]):
                clicked=id
                break
        id+=1
    if return_hover:
        return clicked,hoverid
    else:
        return clicked
def drawRhomboid(surf, color, x, y, width, height, offset, thickness=0):
    points = (
        (x + offset, y), 
        (x + width + offset, y), 
        (x + width-offset, y + height), 
        (x-offset, y + height))
    #pygame.draw.polygon(surf, color, points, thickness)
    pygame.gfxdraw.filled_polygon(surf,points,color)
    pygame.gfxdraw.aapolygon(surf,points,color)
def center_text(screen,text,pos,type='',colour=(255,255,255)): # Can be used for backward compatability but not recommended!
    if "bold" in type:
        ftype=3
    elif "min" in type:
        ftype=1
    elif "grade" in type:
        ftype=2
    elif "score" in type:
        ftype=4
    else:
        ftype=0
    tmp = getfonts(ftype).render(str(text),  True,  colour)
    relative=pygame.Rect(pos)
    out = tmp.get_rect(center=relative.center)
    screen.blit(tmp,  out)