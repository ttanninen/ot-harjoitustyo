import clock, audioengine, sequencer

# Create new sequence
sequence = sequencer.Sequence(128, [])

# Create new track
track1 = sequencer.Track("/samples/bd01.wav", "BD")

# Create 8-step pattern
track1.add_pattern([1,0,0,0, 1,0,1,0])

# Load track 1 to sequence
sequence.add_track(track1)

running = True

while running:
