
def multiplayer():
    global sysbutton
    if activity==14:
        dq=[]
        dqu=[]
        render('rect', arg=((0,100,w,h-160), hcol[2], False))
        if len(multilist):
            for a in multilist:
                dqu.append(str(a['name'])+' - '+str(a['currently_playing'])+' - '+str(a['current_players'])+'/'+str(a['player_limit']))
            for a in range(1,len(multilist)+1):
                dq.append(((w//2)-300,shopscroll+110+(100*(a-1)),600,90))
        else:
            render('text', text='No rooms are avaliable o-o', arg=((0,0), forepallete,'center'),relative=(w//2,h//2,0,0))
        dqs=menu_draw(dq,dqu,bradius=10,styleid=3,selected_button=sbid)
        render('rect', arg=((0,0,w,100), hcol[0], False))
        render('rect', arg=((0,h-60,w,60), hcol[0], False))
        render('text', text='Multiplayer', arg=((20,20), forepallete,'grade'))
        sysbutton=menu_draw(((-10,h-60,100,60),),('Back',),bradius=0,styleid=3)