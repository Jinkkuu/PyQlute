def print_card(pp,score,name,pos,rank,isgrayed=False,home=False,hide=False):
    if hide or not rank<=0:
        if isgrayed:
            tmp=bgdefaultcolour[0]-15,bgdefaultcolour[1]-15,bgdefaultcolour[2]-15
            tmpt=150,150,150
        else:
            tmp=bgdefaultcolour[0]+25,bgdefaultcolour[1]+25,bgdefaultcolour[2]+25
            tmpt=forepallete
        if not name:
            name='Guest'
            rank=0
        dim=35
        render('rect',arg=((pos[0],pos[1],300,80),(tmp),False),borderradius=10)
        if rank or hide:
            if pp>0 and not hide:
                render('text', text='#'+str(format(rank,',')), arg=((pos[0]+290,pos[1]+30), (tmp[0]+dim,tmp[1]+dim,tmp[2]+dim),'grade','rtl'))
            if restricted and not hide:
                render('text', text="You are Restricted", arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
            elif hide:
                render('text', text="Offline", arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
            elif pp>0:
                render('text', text=str(format(score,','))+' (Lv. '+str(format(level,','))+')', arg=((pos[0]+10,pos[1]+60), tmpt,'min'))
                render('text', text=str(format(int(pp),','))+'pp', arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
            else:
                render('text', text='Never played', arg=((pos[0]+10,pos[1]+40), tmpt,'min'))
        else:
            render('text', text='Not Logged in', arg=((pos[0]+10,pos[1]+40), tmpt,'min')) # type: ignore
        render('text', text=name, arg=((pos[0]+10,pos[1]+10), tmpt,'bold'))
