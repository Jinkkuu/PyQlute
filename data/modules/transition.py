def transitionprep(act):
    global transani,actto,ismulti
    actto=act
    if actto==1:
        ismulti=0
    transani[1]=1
    transani[0].start()