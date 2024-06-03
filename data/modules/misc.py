def scrollbar(startpos,endsize,search=3,length=5,color=hcol[3]):
    try:
        t=-20
        t=(search/(length))*(endsize[1])
        render('rect', arg=((startpos[0],startpos[1],endsize[0],endsize[1]), hcol[1], False))
        render('rect', arg=((startpos[0],startpos[1]-t,endsize[0],endsize[1]//length), color, False))
    except Exception:
        pass