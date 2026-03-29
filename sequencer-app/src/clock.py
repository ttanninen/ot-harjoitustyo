from pygame import time

### Pygame for demo purposes ###
### Will be replaced with separate thread master clock ###

def tick():
    time.Clock.tick()

def get_ticks():
    time.get_ticks()