topbarcolour=(40,40,40) # default colour for top bar and blades~
maincolour=(45, 25, 71),(65, 45, 91),(75, 55, 101),(109, 104, 186),(37, 21, 59), (82, 56, 115),(111,77,143),(166, 101, 191),(65, 45, 91) # Color Schemes
emblemcolour=(0,0,0) # Text Colour
songselectcolour=(20,20,20)
mapselectetopbarcolour=(116, 69, 161)
mapidlecolour=(76, 46, 99)
scrollfront=(255,255,255)
scrollback=(50,50,50)
rankcolour=(145, 144, 64),(83, 88, 148),(148, 114, 83),(163, 72, 81),(42, 135, 34)
shopscheme = (112, 73, 140)
volcolour = 168, 232, 255
volback = 60,60,100
applicable_colours = [a for a in globals()][8:]
def setcolour(base,val): # Skin purpose!!
    global shopscheme,scrollback,scrollfront,mapidlecolour,mapselectetopbarcolour,songselectcolour,emblemcolour,maincolour,topbarcolour
    if base in applicable_colours:
        code = []
        for a in val.split(','):
            if a.isdigit():
                code.append(int(a))
            else:
                code.append(0)
        code = tuple(code)
        globals()[base] = code