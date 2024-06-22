#!/usr/bin/python3
import os,time,requests,hashlib,sys,pygame
def maxt(t,o):
    if t+o>254:
        return 255
    elif t+o<t:
        return t
    else:
        return t+o
def mint(t,o):
    if t-o<1:
        return 0
    elif t+o>254:
        return 255
    else:
        return t-o
def stopnow():
    global stop
    clear((0,0,0)) # type: ignore
    pygame.display.update() # type: ignore
    stop=1
def cbytes(size): 
    units = ['B',  'KB',  'MB',  'GB',  'TB']
    unit_index = 0

    while size  >=  1000 and unit_index < len(units) - 1:
        size /= 1000
        unit_index += 1

    converted_size = f"{size:.2f} {units[unit_index]}"
    return converted_size
def test(arg, arg2):
    try:
        arg[arg2]
        return True
    except Exception:
        return False
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
ostype=os.name
datapath=os.path.expanduser('~')+'/.qlute/'
if os.path.isdir('./userdata'):
    print('Successfully migrated to '+str(datapath))
    os.rename('./userdata',datapath)
syspath=resource_path('./data/')
modulepath=syspath+'modules/'
forepallete=(255,255,255)
moduletime=time.time()
if os.path.isfile(syspath+'.version'):
    gamever=open(syspath+'.version').read().rstrip("\n")
if os.path.isfile(syspath+'.edition'):
    gameedition=open(syspath+'.edition').read().rstrip("\n")
for a in os.listdir(resource_path(modulepath)):
    if os.path.isfile(resource_path(modulepath+a)):
        tmp=open(resource_path(modulepath+a)).read()
        if not 'bootstrap.py' in a:
            exec(tmp)
moduletime=time.time()-moduletime
if os.path.isfile(resource_path(modulepath+'bootstrap.py')):
        program=open(resource_path(modulepath+'bootstrap.py')).read()
        if "-testmode" in sys.argv:
            import cProfile
            cProfile.run(program)
        else:
            exec(program)
else:
    print('Bootstrap not Found')
