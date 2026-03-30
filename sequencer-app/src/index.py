import sequencer
import os

dirname = os.path.dirname(__file__)

# Create new sequence
sequence = sequencer.Sequence(128, 4)

# Create new track
test_sample = os.path.join(dirname, "samples", "bd01.wav")
track1 = sequencer.Track(test_sample, "BD")

# Create 16-step pattern
track1.set_length(16)

# Write some notes
track1.write_step(0)
track1.write_step(4)
track1.write_step(8)
track1.write_step(12)

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
