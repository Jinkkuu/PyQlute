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
if not "-devmode" in sys.argv:
    devmode=True # Bypasses the sha256sum Checks and open as Normal. Which would make players able to run the game with modified code that I didn't Verify yet.
else:
    devmode=False # This is the Default
for a in os.listdir(resource_path(modulepath)):
    try:
        if not os.path.isdir(resource_path(modulepath+a)):
            tmpr=open(resource_path(modulepath+a),'rb').read()
            tmp=open(resource_path(modulepath+a)).read()
            if not devmode:
                url = "https://api.github.com/repos/pxkidoescoding/Qlute/contents/data/modules/"+str(a)
                response = requests.get(url)
                print(url)
                sha = response.json()["sha"]
                shalocal=hashlib.sha256(tmpr).hexdigest()
                print(shalocal)
            if not 'bootstrap.py' in a:
                exec(tmp)
    except Exception as error:
        print(str(a),error)
        #print('File:'+str(a)+' is Not Verified, Skipping')
        exit()
        os.remove(resource_path(modulepath+a))
moduletime=time.time()-moduletime
if os.path.isfile(resource_path(modulepath+'bootstrap.py')):
        exec(open(resource_path(modulepath+'bootstrap.py')).read())
else:
    print('Bootstrap not Found')
