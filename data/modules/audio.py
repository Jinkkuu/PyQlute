import pygame.mixer,time
pygame.mixer.init()
tick=0
is_running=0
def get_tick():
    return tick
def inc_tick():
    global tick
    tick+=1
def reset_tick():
    global tick
    tick=0
gametime=0
def set_gametime(delay):
    global gametime
    gametime=time.time()+delay
def load_music(value,loop=0):
    global is_running
    pygame.mixer.music.load(value)
    is_running = 1
    pygame.mixer.music.play(loop)
    set_gametime(0)
    reset_tick()
def music_control(value):
    global is_running
    try:
        if value == 0:
            pygame.mixer.music.play()
            is_running = 1
        if value == 1:
            pygame.mixer.music.stop()
            is_running = 0
        elif value == 2:
            pygame.mixer.music.pause()
            is_running = 0
        elif value == 3:
            pygame.mixer.music.unpause()
            is_running = 1
        elif value == 4:
            return is_running
    except pygame.error:
        print('No music is loaded')
def get_pos():
    return (time.time()-gametime)/0.001