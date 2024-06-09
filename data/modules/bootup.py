def logo():
    global activity,gameverfake,logoflashtime,kd,logopos
    if activity==0:
        render('clear',arg=(0,0,0))
        if issigned or restricted:
            transitionprep(1)
        else:
            transitionprep(10)
