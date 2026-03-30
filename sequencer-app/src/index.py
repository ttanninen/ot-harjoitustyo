import sequencer
import time

# Create new sequence
sequence = sequencer.Sequence(128, 4)

# Create new track
track1 = sequencer.Track("sequencer-app/src/samples/bd01.wav", "BD")

# Create 8-step pattern
track1.replace_pattern([1,0,0,0, 1,0,1,0])

# Load track 1 to sequence
sequence.add_track(track1)

print("Test commands:\nP play\nS stop\nE Exit")

while True:
    command = input("Enter command: ")
    if command == "P":
        sequence.play()
    elif command == "S":
        sequence.stop()
    else:
        break
