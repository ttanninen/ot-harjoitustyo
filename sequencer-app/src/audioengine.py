from pygame import mixer

### Using pygame mixer is for testing reasons ###
### More flexible audio library "python-sounddevice" will be added later ###

mixer.init()

def play(sample):
    mixer.play(sample)