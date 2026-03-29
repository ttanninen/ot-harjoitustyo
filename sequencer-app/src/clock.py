from pygame import time

### Pygame for demo purposes ###
### Will be replaced with separate thread master clock ###

clock = time.Clock()

def tick():
    clock.tick()

def get_ticks():
    return time.get_ticks()