import pygame
def main():
    global inputcache
    inputcache = pygame.event.get()
def get_input():
    for event in inputcache:
        yield event