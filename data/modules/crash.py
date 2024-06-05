def crash(text):
    bypass=0
    print(text)
    pygame.mouse.set_visible(True)
    while not bypass:
        fullscreenchk()
        buttonm=((w//4+10, h//4+h//2-40, w//4-20, 30), (w//4+w//2-w//4-5, h//4+h//2-40, w//4-5, 30), )
        buttont=('Continue', 'Exit', )
        render('rect', arg=((w//4, h//4, w//2, h//2), (40, 40, 40), False), borderradius=10)
        render('rect', arg=((w//4+3, h//4+33, w//2-6, h//2-36), (20, 20, 20), False), borderradius=10)
        button=menu_draw(buttonm, text=buttont)
        render('text', text='Sworry!', arg=((w//4+8, h//4+8), forepallete))
        render('text', text=text, arg=((w//4+15, h//4+48), forepallete))
        pygame.display.update((w//4, h//4, w//2, h//2))
        for event in pygame.event.get():
            if event.type  ==  pygame.QUIT:
                stopnow()
                sys.exit()
            if event.type  ==  pygame.MOUSEBUTTONDOWN:
                if button == 1:
                    bypass=1
                elif button == 2:
                    stopnow()
                    sys.exit()